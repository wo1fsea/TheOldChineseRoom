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
import time
from PIL import Image

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QTimer

from core.communication.queue import Queue
from core.config_reader import ConfigReader
from frame_grabber.frame_reader import FrameReader
import zlib


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'monitor'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.init()

        self._frame_reader = FrameReader()
        self._last_time = 0

    def init(self):
        self.setWindowTitle(self.title)

        # Create widget
        self.label = QLabel(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeOut)
        self.timer.start(10)
        self.show()

    def timeOut(self):
        frame = self._frame_reader.read_frame()
        if frame:
            cur_time = time.time()
            interval = cur_time - self._last_time
            self._last_time = cur_time
            self.setWindowTitle("fps: %f" % (1 / interval))
            pixmap = frame.toqpixmap()
            self.label.setPixmap(pixmap)
            self.label.resize(pixmap.width(), pixmap.height())
            self.resize(pixmap.width(), pixmap.height())


def start():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
