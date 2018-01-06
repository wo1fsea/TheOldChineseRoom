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

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer

from core.frame_grabber.frame_reader import FrameReader


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
        self._intervals = []

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
            self._intervals.append(interval)
            total = sum(self._intervals)
            self.setWindowTitle("fps: %f" % (len(self._intervals)/total))
            if total > 1:
                self._intervals.pop(0)
            pixmap = frame.toqpixmap()
            self.label.setPixmap(pixmap)
            self.label.resize(pixmap.width(), pixmap.height())
            self.resize(pixmap.width(), pixmap.height())


def start():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
