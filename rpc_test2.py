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

from core.communication.rpc import remote_method, RPCManager
import time

def main():
    rpcm = RPCManager()

    for i in range(1000):
        rpcm.call_method("a", "dd", "fff")


if __name__ == '__main__':
    main()
