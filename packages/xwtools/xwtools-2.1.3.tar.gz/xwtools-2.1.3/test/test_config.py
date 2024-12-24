# -*- coding: utf-8 -*-
# @Time    : 2024/12/23 18:01
# @Author  : xuwei
# @FileName: test_config.py
# @Software: PyCharm


if __name__ == '__main__':
    import os
    os.environ['CONFIG_FILE'] = 'settings.ini'
    print(os.getenv("CONFIG_FILE"))
    import xwtools as xw

    r = xw.config("mysql", "host")
    print(r)