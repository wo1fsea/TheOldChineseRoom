# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/10/29
Description:
    table_test.py
----------------------------------------------------------------------------"""

from core.communication.table import Table


def main():
    a = Table("A")
    a["1"] = 1
    a["2"] = 2
    a[3] = "3"

    for k in a.keys():
        print(k)
    for it in a.items():
        print(it)

    print(a.get("d", "fff"))

if __name__ == '__main__':
    main()
