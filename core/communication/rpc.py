# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/7
Description:
    rpc.py
----------------------------------------------------------------------------"""

import time
import asyncio
import inspect
import threading

from utils import uuid
from utils.expire_dict import ExpireDict
from utils.singleton import Singleton

from .collections.queue import Queue
from .collections.table import Table

SERVICE_TTL = 30 * 1000  # milliseconds
SERVICE_HEARTBEAT_INTERVAL = SERVICE_TTL // 2  # milliseconds

BGET_TIMEOUT = SERVICE_TTL // 1000  # seconds
ASYNC_GET_POLL_INTERVAL = 0.1  # seconds

RPC_SERVICE_TABLE_KEY = "global_service_table"

RPC_ID_PREFIX = "rpc_"
SERVICE_ID_PREFIX = "service_"
REQUEST_QUEUE_ID_PREFIX = "request_queue_"

DEFAULT_RPC_DATA = {
    "rpc_id": None,
    "method_name": "",
    "args": [],
    "kwargs": {},
    "return_value": None,
    "exception": None,

    "request_time": None,
    "return_time": None,
}

DEFAULT_SERVICE_DATA = {
    "service_id": None,
    "service_name": "",
    "method_list": [],

    "request_queue_id": None,

    "register_time": None
}


class RPCManager(Singleton):
    @staticmethod
    def gen_service_uuid():
        return SERVICE_ID_PREFIX + uuid.generate_uuid()

    @staticmethod
    def gen_rpc_uuid():
        return RPC_ID_PREFIX + uuid.generate_uuid()

    @staticmethod
    def gen_request_queue_uuid():
        return REQUEST_QUEUE_ID_PREFIX + uuid.generate_uuid()

    def __init__(self):
        self._service_map = Table(RPC_SERVICE_TABLE_KEY)
        self._request_queue_cache = ExpireDict(SERVICE_TTL)

    def register_service(self, service_name, method_name_list, enable_multi_instance=True):
        service_id = self._service_map.setdefault(service_name, self.gen_service_uuid())
        service_data = Table(service_id)

        if not service_data.exists:
            service_data["service_id"] = service_id
            service_data["request_queue_id"] = self.gen_request_queue_uuid()
            service_data["service_name"] = service_name
            service_data["method_list"] = method_name_list
            service_data["register_time"] = service_data.time
        else:
            assert enable_multi_instance, "service instance already exist."

        assert service_data["method_list"] == method_name_list, "can not register same service with different methods."

        service_data.set_expire(SERVICE_TTL)

    def service_heartbeat(self, service_name):
        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)
        service_data.set_expire(SERVICE_TTL)

    def get_services(self):
        return self._service_map.keys()

    def get_method_list(self, service_name):
        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)

        assert service_data.exists, "service invalid."
        return service_data.get("method_list")

    def _get_request_queue(self, service_name):
        request_queue = self._request_queue_cache.get(service_name)
        if request_queue:
            return request_queue

        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)
        assert service_data.exists, "service expired."
        request_queue = Queue(service_data["request_queue_id"])

        self._request_queue_cache[service_name] = request_queue
        return request_queue

    def _push_request(self, service_name, method_name, args, kwargs):
        request_queue = self._get_request_queue(service_name)

        rpc_data = dict(DEFAULT_RPC_DATA)
        rpc_id = self.gen_rpc_uuid()
        rpc_data["rpc_id"] = rpc_id
        rpc_data["method_name"] = method_name
        rpc_data["args"] = args
        rpc_data["kwargs"] = kwargs
        rpc_data["request_time"] = self._service_map.time

        request_queue.put(rpc_data)
        return rpc_id

    def _pop_result(self, rpc_data):
        if not rpc_data:
            raise Exception("service timeout")

        return_value = rpc_data["return_value"]
        exception = rpc_data["exception"]

        if exception:
            raise exception

        return return_value

    def call_method(self, service_name, method_name, args, kwargs):
        rpc_id = self._push_request(service_name, method_name, args, kwargs)

        # block until return
        result_queue = Queue(rpc_id)
        rpc_data = result_queue.bget(BGET_TIMEOUT)
        result_queue.clear()

        return self._pop_result(rpc_data)

    async def async_call_method(self, service_name, method_name, args, kwargs):
        rpc_id = self._push_request(service_name, method_name, args, kwargs)

        # block until return
        rpc_data = None
        result_queue = Queue(rpc_id)
        request_time = time.time()
        while rpc_data is None:
            if time.time() - request_time > BGET_TIMEOUT:
                break
            await asyncio.sleep(ASYNC_GET_POLL_INTERVAL)
            rpc_data = result_queue.get()

        result_queue.clear()
        return self._pop_result(rpc_data)

    def handle_call_request(self, remote_methods, rpc_data):
        request_time = rpc_data["request_time"]

        if self._service_map.time - request_time > SERVICE_TTL:
            return

        rpc_id = rpc_data["rpc_id"]
        method_name = rpc_data["method_name"]
        args = rpc_data["args"]
        kwargs = rpc_data["kwargs"]
        return_value = None
        exception = None
        method = remote_methods[method_name]

        try:
            return_value = method(*args, **kwargs)

        except Exception as ex:
            exception = ex

        rpc_data["return_value"] = return_value
        rpc_data["exception"] = exception

        return_queue = Queue(rpc_id, max_len=1)
        return_queue.put(rpc_data)

    def get_request_data(self, service_name):
        request_queue = self._get_request_queue(service_name)
        return request_queue.bget(BGET_TIMEOUT)


def remote_method(method):
    frame = inspect.currentframe()
    # class_name = frame.f_back.f_code.co_names
    method_name = method.__code__.co_name
    rpc_methods = frame.f_back.f_locals.setdefault("rpc_methods", [])
    rpc_methods.append(method_name)

    return method


class RPCService(object):
    rpc_methods = []

    def __init__(self, enable_multi_instance=True):
        self._rpc_manager = RPCManager()
        self._remote_methods = {}
        self._is_running = False
        self._heartbeat_thread = None
        self._process_thread = None
        self._enable_multi_instance = enable_multi_instance

    @property
    def service_name(self):
        return self.__class__.__name__

    def start(self):
        self.register_methods()
        self._is_running = True
        self.start_heartbeat()
        self.start_process()

    def stop(self):
        self._is_running = False
        self.stop_heartbeat()
        self.stop_process()

    def register_methods(self):
        self._rpc_manager.register_service(self.service_name, self.rpc_methods, self._enable_multi_instance)
        for name in self.rpc_methods:
            method = getattr(self, name)
            self._remote_methods[name] = method

    def _process(self):
        while self._is_running:
            request_data = self._rpc_manager.get_request_data(self.service_name)
            if request_data:
                self._rpc_manager.handle_call_request(self._remote_methods, request_data)

    def start_process(self):
        assert self._process_thread is None, "process thread is already running."
        self._process_thread = threading.Thread(target=self._process)
        self._process_thread.start()

    def stop_process(self):
        assert self._process_thread is not None, "process thread is not running."
        self._process_thread.join()
        self._process_thread = None

    def _heartbeat(self):
        while self._is_running:
            self._rpc_manager.service_heartbeat(self.service_name)
            time.sleep(SERVICE_HEARTBEAT_INTERVAL // 1000)

    def start_heartbeat(self):
        assert self._process_thread is None, "heartbeat thread is already running."
        self._heartbeat_thread = threading.Thread(target=self._heartbeat)
        self._heartbeat_thread.start()

    def stop_heartbeat(self):
        assert self._heartbeat_thread is not None, "heartbeat thread is not running."
        self._heartbeat_thread.join()
        self._heartbeat_thread = None


class RPCClientMethod(object):
    def __init__(self, rpc_manager, service_name, method_name):
        super(RPCClientMethod, self).__init__()
        self._rpc_manager = rpc_manager
        self._service_name = service_name
        self._method_name = method_name

    def __call__(self, *args, **kwargs):
        return self._rpc_manager.call_method(self._service_name, self._method_name, args, kwargs)


class AsyncRPCClientMethod(object):
    def __init__(self, rpc_manager, service_name, method_name):
        super(AsyncRPCClientMethod, self).__init__()
        self._rpc_manager = rpc_manager
        self._service_name = service_name
        self._method_name = method_name

    async def __call__(self, *args, **kwargs):
        return await self._rpc_manager.async_call_method(self._service_name, self._method_name, args, kwargs)


class RPCClient(object):
    def __init__(self, service_name):
        super(RPCClient, self).__init__()
        self._service_name = service_name
        self._rpc_manager = RPCManager()

        assert service_name in self._rpc_manager.get_services(), "service not found."
        self._method_list = self._rpc_manager.get_method_list(service_name)

    @property
    def service_name(self):
        return self.service_name

    def __getattr__(self, method_name):
        if self._method_list and method_name in self._method_list:
            return RPCClientMethod(self._rpc_manager, self._service_name, method_name)
        raise AttributeError("type object '%s' has no attribute '%s'" % (self.__class__.__name__, method_name))


class AsyncRPCClient(object):
    def __init__(self, service_name):
        super(AsyncRPCClient, self).__init__()
        self._service_name = service_name
        self._rpc_manager = RPCManager()

        assert service_name in self._rpc_manager.get_services(), "service not found."
        self._method_list = self._rpc_manager.get_method_list(service_name)

    @property
    def service_name(self):
        return self.service_name

    def __getattr__(self, method_name):
        if self._method_list and method_name in self._method_list:
            return AsyncRPCClientMethod(self._rpc_manager, self._service_name, method_name)
        raise AttributeError("type object '%s' has no attribute '%s'" % (self.__class__.__name__, method_name))
