#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-12-17 20:29:11
# @Author: Alan
# @File: work_mondodb.py
# @Describe:

import os
import yaml
import contextlib
from pymongo import MongoClient


@contextlib.contextmanager
def init_mongodb(host, port, username=None, password=None):
    try:
        if username and password:
            conn = MongoClient(
                host=host,
                port=port,
                username=username,
                password=password
            )
        else:
            conn = MongoClient(
                host=host,
                port=port
            )
        yield conn
    except Exception as e:
        print(str(e))
        print('init mongodb failed...')
    finally:
        conn.close()


def create_db_and_coll(config, database_name, coll_name):
    """
    在 MongoDB 中,数据库只有在内容插入后才会创建! 就是说,数据库创建后要创建集合(数据表)并插入一个文档(记录),数据库才会真正创建
    下面的代码 优先判断database_name和coll_name是否已创建
    """
    try:
        with init_mongodb(config['HOST'], config['PORT']) as conn:
            all_databases = conn.list_database_names()
            if database_name in all_databases:  # 判断database_name 是否已创建
                # coll_name 是否已创建
                if coll_name not in conn[database_name].list_collection_names():
                    conn[database_name].create_collection(coll_name)
                else:
                    print('{}集合已存在...'.format(coll_name))
                    return
            else:
                conn[database_name].create_collection(coll_name)
    except Exception as e:
        pass


def get_collections(config, database_name):
    """
    某个数据库的全部集合
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        coll_names = db.list_collection_names()
    return coll_names


def insert_data(config, database_name, collection_name, data):
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)


def find_coll_one(config, database_name, collection_name, query_data):
    """
    查询合集里指定的数据
    query_data是查询的关键字
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        datas = [i for i in collection.find(query_data)]
        return datas


def find_coll_all(config, database_name, collection_name):
    """
    查询合集里全部的数据
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        datas = [i for i in collection.find()]
        return datas


def find_coll_limit_data(config, database_name, collection_name, count):
    """
    查询合集里全部的数据, 返回指定条数的数据
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        datas = [i for i in collection.find().limit(count)]
        return datas


def find_coll_skip_data(config, database_name, collection_name, skip_count, limit_count):
    """
    查询合集里全部的数据, 返回指定条数的数据
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        datas = [i for i in collection.find().skip(
            skip_count).limit(limit_count)]
        return datas


def sort_coll_data(config, database_name, collection_name, account_name, sort_type=1):
    """
    查询合集里全部的数据, 返回指定条数的数据
    """
    with init_mongodb(config['HOST'], config['PORT']) as conn:
        db = conn[database_name]
        collection = db.get_collection(collection_name)
        datas = [i for i in collection.find().sort(account_name, sort_type)]
        return datas
