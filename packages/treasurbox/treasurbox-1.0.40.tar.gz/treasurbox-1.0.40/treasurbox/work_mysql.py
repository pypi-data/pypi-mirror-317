#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-11-04 14:39:13
# @Author: Alan
# @File: work_mysql.py
# @Describe: work for mysql

import pymysql


@contextlib.contextmanager
def my_db(host, port, username, password, db, charset='utf8'):
    conn = pymysql.connect(
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


def get_data_one(config, sql):
    """
    get database one data
    config like CONFIG['local']
    """
    with my_db(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
        cursor.execute(sql)
        all_data = cursor.fetchall()
        if all_data:
            return all_data[0]
        else:
            print('No data found...')


def get_data_all(config, sql):
    """
    get database all data
    """
    with my_db(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
        cursor.execute(sql)
        all_data = cursor.fetchall()
        if all_data:
            return list(all_data)
        else:
            print('No data found...')


def insert_or_update_data(config, sql):
    """
    insert database one data
    """
    try:
        with my_db(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
            cursor.execute(sql)
    except Exception as e:
        print(str(e))


def insert_data_list(config, sql, data):
    """
    insert a list data.
    data like [[...],[...],[...]]
    """
    try:
        with my_db(config['HOST'], config['PORT'], config['USERNAME'], config['PASSWORD'], config['DATABASE']) as cursor:
            cursor.executemany(sql, data)
    except Exception as e:
        print(str(e))
