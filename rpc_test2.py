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

from core.communication.rpc import remote_method, RPCManager, RPCClient, AsyncRPCClient
import time
import asyncio

def main():
    aa = RPCClient("a")

    for i in range(10):
        print(aa.dd("fff"))

async def main2():
    aa = AsyncRPCClient("a")
    async def pf():
        r = await aa.dd(ff="fff")
        print(r)
    await asyncio.wait([pf() for i in range(1000)])


if __name__ == '__main__':
    # main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main2())