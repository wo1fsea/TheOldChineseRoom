# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/6
Description:
    monitor.py
----------------------------------------------------------------------------"""

import sys
from PIL import Image

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import QTimer

from core.communication.queue import Queue
from core.config_reader import ConfigReader


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'monitor'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.init()

        config = ConfigReader().get_config("frame_capture")
        self._queue = Queue(config["frame_cache_key"], config["frame_cache_length"])

    def init(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create widget
        self.label = QLabel(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeOut)
        self.timer.start(10)
        self.show()

    def timeOut(self):
        data = self._queue.get()
        if data:
            size, bytes = eval(data)
            frame = Image.frombytes('RGB', size, bytes)
            pixmap = frame.toqpixmap()
            self.label.setPixmap(pixmap)
            self.label.resize(pixmap.width(), pixmap.height())
            self.resize(pixmap.width(), pixmap.height())


def start():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
