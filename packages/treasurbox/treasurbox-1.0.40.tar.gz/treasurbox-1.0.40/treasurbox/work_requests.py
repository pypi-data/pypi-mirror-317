#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-23 18:40:38
# @Author: Alan
# @File: work_requests.py
# @Describe: common requests

import os
import datetime
import requests
from loguru import logger


def generate_now():
    """
    demo: 20241126141711
    """
    time_now = datetime.datetime.now()
    res = time_now.strftime('%Y%m%d%H%M%S')
    return str(res)


def generate_log(file=False, path=False):
    """
    use loguru make log
    path please wait, default local logs dir
    """
    logger.remove()
    if file:
        # log path and name
        log_file = os.path.join(log_dir, 'test_{}.log'.format(generate_now()))
        logger.configure(handlers=[
            {
                "sink": sys.stderr,
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | <lvl>{level}</> | {module}:{line:3} | <lvl>{message}</>",
                # "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |<lvl>{level:8}</>| {name} : {module}:{line:4} | <cyan>{extra[module_name]}</> | - <lvl>{message}</>",
                "colorize": True,
            },
            {
                "sink": '{}'.format(log_file),
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{line:3} | {message}",
                "colorize": False,
                "rotation": "10 MB",
                "retention": "30 days",
                "compression": "zip",
                "backtrace": True,
                "diagnose": True,
                "encoding": "utf-8",
                "enqueue": True
            }
        ])
    else:
        logger.configure(handlers=[
            {
                "sink": sys.stderr,
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | <lvl>{level}</> | {module}:{line:3} | <lvl>{message}</>",
                # "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |<lvl>{level:8}</>| {name} : {module}:{line:4} | <cyan>{extra[module_name]}</> | - <lvl>{message}</>",
                "colorize": True,
            }
        ])
    return logger


def common_requests(url, header=None, data=None, proxies=None, http_method='GET', file=False):
    """
    include POST and GET
    if file=True  will be save the log into the logfile
    """
    if file:
        logger = generate_log(file=True)
    else:
        logger = generate_log()
    try:
        if http_method.upper() == 'GET':
            res = requests.get(
                url, params=data, headers=header, timeout=(9, 30), proxies=proxies, verify=False)
            logger.info('>>>> request: ')
            logger.info('>>>> url: {}'.format(url))
            logger.info('>>>> header: {}'.format(header))
            logger.info('>>>> params: {}'.format(data))
            return res.json()
        else:
            res = requests.post(
                url, data=data, headers=header, timeout=(9, 30), proxies=proxies, verify=False)
            logger.info('>>>> request: ')
            logger.info('>>>> url: {}'.format(url))
            logger.info('>>>> header: {}'.format(header))
            logger.info('>>>> data: {}'.format(data))
            return res.json()
    except Exception as e:
        print(e)
