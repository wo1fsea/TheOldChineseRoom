# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/4
Description:
    main.py
----------------------------------------------------------------------------"""

from subprocess import Popen, PIPE


def main():
    redis = Popen(['python3', './launcher.py', 'redis_docker'], stdout=PIPE, stderr=PIPE)
    frame_capture = Popen(['python3', './launcher.py', 'frame_grabber'], stdout=PIPE, stderr=PIPE)
    monitor = Popen(['python3', './launcher.py', 'monitor'], stdout=PIPE, stderr=PIPE)


if __name__ == '__main__':
    main()

