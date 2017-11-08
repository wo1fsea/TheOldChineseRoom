# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/8
Description:
    rpc_test2.py
----------------------------------------------------------------------------"""

from core.communication.rpc import remote_method, RPCManager, RPCClient
import time


def main():
    aa = RPCClient("a")

    for i in range(1000):
        print(aa.dd("fff"))


if __name__ == '__main__':
    main()
