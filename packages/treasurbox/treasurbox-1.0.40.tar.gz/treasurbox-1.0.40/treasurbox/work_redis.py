#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-17 20:35:33
# @Author: Alan
# @File: work_redis.py
# @Describe:

import redis
import contextlib


@contextlib.contextmanager
def init_redis(host, port, password, db, ssl=False):
    if ssl:
        conn = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db,
            ssl=True
        )
    elif password:
        conn = redis.Redis(
            host=host,
            port=port,
            password=password,
            db=db
        )
    else:
        conn = redis.Redis(
            host=host,
            port=port,
            db=db
        )
    try:
        yield conn
    except Exception as e:
        print('redis conn error: {}'.format(e))
    finally:
        conn.quit()


def add_redis_data(config, key, value, expire_time=604800):
    """
    insert into redis
    """
    with init_redis(config['redis']['url'], config['redis']['port'], config['redis']['passwd'], config['redis']['db']) as conn:
        conn.set(key, value, ex=expire_time)


def get_redis_data(config, key):
    """
    get data from redis
    """
    with init_redis(config['redis']['url'], config['redis']['port'], config['redis']['passwd'], config['redis']['db']) as conn:
        conn.get(key)


def add_redis_batch_data(config, data, expire_time=604800):
    """
    # batch insert datas like:
    data = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'
    }
    r.mset(data)
    """
    with init_redis(config['url'], config['port'], config['passwd'], config['db']) as conn:
        conn.mset(data)
        # everyone config a expire_time
        for key in data.keys():
            conn.expire(key, expire_time)
