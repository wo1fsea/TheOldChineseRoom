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
    rpcm.call_method("print0", [])
    rpcm.call_method("print0", {})
    rpcm.call_method("print1", "a")
    rpcm.call_method("print1", ["b"])
    rpcm.call_method("print2", {"p1": 1, "p2": 2})

if __name__ == '__main__':
    main()
