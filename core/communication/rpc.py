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

RPC_MANAGER_KEY = "GLOBAL"
RPC_ID_PREFIX = "rpc_"



DEFAULT_RPC_DATA = {
    "rpc_id": None,
    "method_name": "",
    "params": [],
    "return_value": None,
    "exception": None,
}


class RPCManager(Singleton):
    def __init__(self, key=RPC_MANAGER_KEY):
        self._key = key
        self._remote_methods = {}
        self._rpc_request_queue = Queue(self._key)

    def register_method(self, method_name, method):
        assert method_name not in self._remote_methods, "same method name (%s) already exists." % method_name
        self._remote_methods[method_name] = method

    def call_method(self, method_name, params):
        # ToDo: check method name in db

        rpc_data = dict(DEFAULT_RPC_DATA)
        rpc_id = RPC_ID_PREFIX + uuid.generate_uuid()
        rpc_data["rpc_id"] = rpc_id
        rpc_data["method_name"] = method_name
        rpc_data["params"] = params
        self._rpc_request_queue.put(rpc_data)
        rpc_data = Queue(rpc_id).bget()
        return_value = rpc_data["return_value"]
        exception = rpc_data["exception"]

        if exception:
            raise eval(exception)

        return return_value

    def handle_call_request(self):
        rpc_data = self._rpc_request_queue.bget()
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

    def handle_loop(self):
        while True:
            self.handle_call_request()


def remote_method(method):
    method_name = method.__code__.co_name
    rpc_manager = RPCManager()
    rpc_manager.register_method(method_name, method)
