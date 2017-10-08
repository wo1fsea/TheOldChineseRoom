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

from core.communication.rpc import RPCManager


def main():
    def print_test0():
        print("print_text0")

    def print_test1(p1):
        print("print_text1", p1)

    def print_test2(p1, p2):
        print("print_text2", p1, p2)

    rpcm = RPCManager()
    rpcm.register_method("print0", print_test0)
    rpcm.register_method("print1", print_test1)
    rpcm.register_method("print2", print_test2)
    rpcm.handle_loop()


if __name__ == '__main__':
    main()
