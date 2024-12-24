#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-11-05 11:27:16
# @Author: Alan
# @File: work_decorator
# @Describe: used time decorator

import time
import logging
from decorator import decorator


@decorator
def time_used(func, timelimit=60, *args, **kw):
    t0 = time.time()
    result = func(*args, **kw)
    dt = time.time() - t0
    print('time used: {}s'.format(round(dt, 2)))
    if dt > timelimit:
        logging.warning('%s took %d seconds', func.__name__, dt)
    else:
        logging.info('%s took %d seconds', func.__name__, dt)
    return result
