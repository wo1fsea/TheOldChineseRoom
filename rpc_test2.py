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


def main():
    @remote_method
    def print_test0():
        print("print_text0")
        return "print0"

    @remote_method
    def print_test1(p1):
        print("print_text1", p1)
        return "print1"

    @remote_method
    def print_test2(p1, p2):
        print("print_text2", p1, p2)
        raise Exception("DDD")

    rpcm = RPCManager()
    rpcm.handle_loop()


if __name__ == '__main__':
    main()
