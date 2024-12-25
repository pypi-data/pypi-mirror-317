#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-05-31 14:39:31
# @Author: Alan
# @File: work_yaml.py
# @Describe: work for yaml

import yaml


class DoYaml:
    def __init__(self, filename):
        self.filename = filename

    def read_config(self, filename):
        """
        read data from yaml file
        """
        with open(self.filename, 'r') as yaml_file:
            dic_yaml = yaml.load(yaml_file.read(), Loader=yaml.FullLoader)
            return dic_yaml
