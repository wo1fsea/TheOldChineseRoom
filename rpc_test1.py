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

from core.communication.rpc import RPCManager, RPCService, remote_method


def main():
    class a(RPCService):
        @remote_method
        def dd(self, ff):
            print(ff)
            return ff

    aa = a()
    aa.start()


if __name__ == '__main__':
    main()
