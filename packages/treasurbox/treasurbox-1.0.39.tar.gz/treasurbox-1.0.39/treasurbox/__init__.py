#!/usr/bin/env Python
# _*_coding:utf-8 _*_

# from work_mysql import get_data_one, get_data_all, insert_or_update_data, insert_data_list
# from src.work_mysql import get_data_one, get_data_all, insert_or_update_data, insert_data_list
# from src.work_yaml import DoYaml, read_config
# from src.work_decorator import time_used

"""
Mysql:
input: config
eg:
CONFIG = read_config()
config = CONFIG['local']

get_data_one(config, sql)
get_data_all(config, sql)
insert_or_update_data(config, sql)
insert_data_list(config, sql)
"""

"""
Yaml:
eg:
my_yaml=DoYaml(filename)
res=my_yaml.read_config()
"""
__all__ = ["DoYaml", "read_config", "get_data_one",
           "get_data_all", "insert_or_update_data", "insert_data_list", "time_used", "FakerMaker"]
