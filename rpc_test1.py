# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/8
Description:
    rpc_test1.py
----------------------------------------------------------------------------"""

from core.communication.rpc import RPCManager


def main():
    rpcm = RPCManager()
    print(rpcm.register_method.__code__.co_name)
    print(rpcm.call_method("print_test0", []))
    print(rpcm.call_method("print_test0", {}))
    print(rpcm.call_method("print_test1", "a"))
    print(rpcm.call_method("print_test1", ["b"]))
    print(rpcm.call_method("print_test2", {"p1": 1, "p2": 2}))

if __name__ == '__main__':
    main()
