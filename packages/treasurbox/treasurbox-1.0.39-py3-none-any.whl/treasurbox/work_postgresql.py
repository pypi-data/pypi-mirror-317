#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-24 15:53:15
# @Author: Alan
# @File: work_postgresql.py
# @Describe: work for postgresql

import contextlib
import psycopg2


@contextlib.contextmanager
def my_postgresql(host, port, username, password, db, charset='utf8'):
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=username,
        passwd=password,
        db=db,
        charset=charset)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def update_data(config, sql):
    """
    query data
    """
    try:
        with my_postgresql(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
            cursor.execute(sql)
    except Exception as e:
        print(str(e))


def query_data(config, sql):
    """
    get database data
    """
    with my_postgresql(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
        cursor.execute(sql)
        all_data = cursor.fetchall()
        if all_data:
            return all_data
        else:
            print('没有查到数据库数据')
