# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2018/1/13
Description:
	watcher
----------------------------------------------------------------------------"""

from utils.singleton import Singleton
from ..communication.rpc import RPCService


class WatcherService(RPCService):
	def __init__(self):
		super(WatcherService, self).__init__()


class Watcher(Singleton):
	def __init__(self):
		pass

	def set_status(self, status):
		pass

	def log(self, log_message):
		pass

	def register_commands(self, commands):
		pass

	def start_watcher_service(self):
		pass

	def stop_watcher_service(self):
		pass
