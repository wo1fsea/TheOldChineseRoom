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

from utils.singleton import Singleton
from utils import uuid
from .queue import Queue
from .table import Table

SERVICE_TTL = 30 * 1000
SERVICE_HEARTBEAT_INTERVAL = SERVICE_TTL / 2

RPC_SERVICE_TABLE_KEY = "global_service_table"

RPC_ID_PREFIX = "rpc_"
SERVICE_ID_PREFIX = "service_"
REQUEST_QUEUE_ID_PREFIX = "request_queue_"

DEFAULT_RPC_DATA = {
    "rpc_id": None,
    "method_name": "",
    "params": [],
    "return_value": None,
    "exception": None,

    "request_time": None,
    "return_time": None,
}

DEFAULT_SERVICE_DATA = {
    "service_id": None,
    "service_name": "",
    "method_list": [],

    "request_queue_id": "",

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
        self._remote_methods = {}
        self._service_map = Table(RPC_SERVICE_TABLE_KEY)

    def register_service(self, service_name, method_name_list, enable_multi_instance=True):
        service_id = self._service_map.get(service_name, self.gen_service_uuid())
        service_data = Table(service_id)

        if not service_data.exists():
            service_data["service_id"] = service_id
            service_data["request_queue_id"] = self.gen_request_queue_uuid()
            service_data["service_name"] = service_name
            service_data["method_list"] = method_name_list
            service_data["register_time"] = service_data.time()

        assert service_data["method_list"] == method_name_list, "can not register same service with different methods."

        service_data.set_expire(SERVICE_TTL)

    def service_heartbeat(self, service_name):
        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)
        service_data.set_expire(SERVICE_TTL)

    def get_services(self):
        return self._service_map.keys()

    def register_method(self, method_name, method):
        assert method_name not in self._remote_methods, "same method name (%s) already exists." % method_name
        self._remote_methods[method_name] = method

    def call_method(self, service_name, method_name, params):
        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)
        assert service_data.exists(), "service expired."
        request_queue = Queue(service_data["request_queue_id"])

        rpc_data = dict(DEFAULT_RPC_DATA)
        rpc_id = self.gen_rpc_uuid()
        rpc_data["rpc_id"] = rpc_id
        rpc_data["method_name"] = method_name
        rpc_data["params"] = params
        rpc_data["request_time"] = request_queue.time()

        request_queue.put(rpc_data)

        # block until return
        rpc_data = Queue(rpc_id).bget()
        return_value = rpc_data["return_value"]
        exception = rpc_data["exception"]

        if exception:
            raise eval(exception)

        return return_value

    def handle_call_request(self, request_queue):
        rpc_data = request_queue.bget()
        if rpc_data:
            rpc_id = rpc_data["rpc_id"]
            method_name = rpc_data["method_name"]
            params = rpc_data["params"]
            return_value = None
            exception = None
            method = self._remote_methods[method_name]

            try:
                if isinstance(params, dict):
                    return_value = method(**params)
                elif isinstance(params, (tuple, list)):
                    return_value = method(*params)
                else:
                    return_value = method(params)

            except Exception as ex:
                exception = ex.__repr__()

            rpc_data["return_value"] = return_value
            rpc_data["exception"] = exception

            return_queue = Queue(rpc_id, max_len=1)
            return_queue.put(rpc_data)

    def handle_loop(self, service_name):
        service_id = self._service_map.get(service_name)
        assert service_id, "service not found."

        service_data = Table(service_id)
        assert service_data.exists(), "service expired."
        request_queue = Queue(service_data["request_queue_id"])

        while True:
            self.handle_call_request(request_queue)


def remote_method(method):
    method_name = method.__code__.co_name
    rpc_manager = RPCManager()
    rpc_manager.register_method(method_name, method)
