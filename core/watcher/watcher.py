# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2018/1/13
Description:
    watcher.py
----------------------------------------------------------------------------"""

from utils.singleton import Singleton
from ..communication.rpc import RPCService, RPCClient, remote_method
from ..communication.collections.queue import Queue
from ..communication.collections.dict import Dict

WATCHER_COMMAND_SERVICE_NAME = "watcher_command_%s"
WATCHER_LOG_QUEUE_KEY = "watcher_log_%s"
WATCHER_STATUS_DICT_KEY = "watcher_status_%s"


class WatcherCommandService(RPCService):
    def __init__(self, serivce_name):
        super(WatcherCommandService, self).__init__(serivce_name)
        self._commands = {}

    def register_commands(self, commands):
        self._commands = commands

    @remote_method
    def get_commands(self):
        return list(self._commands.keys())

    @remote_method
    def run_command(self, command, *args, **kwargs):
        command_func = self._commands.get(command)
        if command_func:
            return command_func(*args, **kwargs)
        else:
            return None


class Watcher(Singleton):
    def __init__(self, watcher_key):
        super(Watcher, self).__init__()
        self._watcher_key = watcher_key
        self._watcher_command_service = WatcherCommandService(WATCHER_COMMAND_SERVICE_NAME % watcher_key)
        self._log = Queue(WATCHER_LOG_QUEUE_KEY % self._watcher_key)
        self._status = Dict(WATCHER_STATUS_DICT_KEY % self._watcher_key)

        self._status.clear()

    def set_status(self, status):
        self._status.update(status)

    def log(self, log_message):
        self._log.put(log_message)

    def register_commands(self, commands):
        self._watcher_command_service.register_commands(commands)

    def start_watcher_command_service(self):
        self._watcher_command_service.start()

    def stop_watcher_command_service(self):
        self._watcher_command_service.stop()


class WatcherClient(object):
    def __init__(self, watcher_key):
        super(WatcherClient, self).__init__()
        self._watcher_key = watcher_key
        self._watcher_command_service = RPCClient(WATCHER_COMMAND_SERVICE_NAME % watcher_key)
        self._log = Queue(WATCHER_LOG_QUEUE_KEY % self._watcher_key)
        self._status = Dict(WATCHER_STATUS_DICT_KEY % self._watcher_key)

    def get_status(self):
        return dict(self._status)

    def get_logs(self, num=0):
        raise NotImplementedError()

    def get_commands(self):
        return self._watcher_command_service.get_commands()

    def run_command(self, command, *args, **kwargs):
        return self._watcher_command_service.run_command(command, *args, **kwargs)
