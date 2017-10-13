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

RPC_ID_PREFIX = "rpc_"
RPC_REQUEST_QUEUE_KEY = "rpc_request"

DEFAULT_RPC_DATA = {
    "rpc_id": None,
    "method_name": "",
    "params": [],
    "return_value": None,
    "error": None,
}

MAX_HANDLE_INTERVAL = 0.1


class RPCManager(Singleton):
    def __init__(self):
        self._remote_methods = {}
        self._rpc_request_queue = Queue(RPC_REQUEST_QUEUE_KEY)

    def register_method(self, method_name, method):
        assert method_name not in self._remote_methods, "same method name (%s) already exists." % method_name
        self._remote_methods[method_name] = method

    def call_method(self, method_name, params):
        # ToDo: check method name in db

        rpc_data = dict(DEFAULT_RPC_DATA)
        rpc_data["rpc_id"] = RPC_ID_PREFIX + uuid.generate_uuid()
        rpc_data["method_name"] = method_name
        rpc_data["params"] = params
        self._rpc_request_queue.put(rpc_data)

    def handle_call_request(self):
        rpc_data = self._rpc_request_queue.bget()
        if rpc_data:
            rpc_id = rpc_data["rpc_id"]
            method_name = rpc_data["method_name"]
            params = rpc_data["params"]
            return_value = None
            error = None
            method = self._remote_methods[method_name]

            try:
                if isinstance(params, dict):
                    return_value = method(**params)
                elif isinstance(params, (tuple, list)):
                    return_value = method(*params)
                else:
                    return_value = method(params)

            except Exception as ex:
                error = str(ex)

            rpc_data["return_value"] = return_value
            rpc_data["error"] = error

            return_queue = Queue(rpc_id, max_len=1)
            return_queue.put(rpc_data)

    def handle_loop(self):
        while True:
            self.handle_call_request()


def remote_method():
    pass
