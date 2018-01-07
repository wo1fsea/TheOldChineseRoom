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
import time
i = 0
def main():
    class a(RPCService):
        @remote_method
        def dd(self, ff):
            global i
            # time.sleep(1)
            i += 1
            # if i == 1000:
            #     exit(0)
            # raise Exception("d")
            print(ff)
            return ff

    aa = a()
    aa.start()
    aa.stop()


if __name__ == '__main__':
    main()
