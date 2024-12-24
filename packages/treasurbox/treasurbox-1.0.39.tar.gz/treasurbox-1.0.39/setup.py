#!/usr/bin/env Python
# _*_coding:utf-8 _*_
# @Time: 2024-05-31 14:36:04
# @Author: Alan
# @File: setup.py
# @Describe: setup work

import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="treasurbox",  # 用自己的名替换其中的YOUR_USERNAME_
    version="1.0.39",  # 包版本号，便于维护版本,保证每次发布都是版本都是唯一的
    author="Alan",  # 作者，可以写自己的姓名
    author_email="linanaicyt@163.com",  # 作者联系方式，可写自己的邮箱地址
    description="A small example package",  # 包的简述
    license='MIT',
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    keywords=['Mysql', 'Python', 'decorator'],
    # url="https://github.com/Lvan826199/mwjApiTest",  # 自己项目地址，比如github的项目地址
    install_requires=[
        "requests",
        "pyyaml",
        "pymysql",
        "decorator",
        "faker>=30.8.2",
        "fake_useragent>=1.5.1",
        "numpy>=2.0.2",
        "contextlib",
        "pymongo",
        "redis",
        "loguru",
        "jsonpath"
    ],
    # packages=setuptools.find_packages(where='src'),
    packages=setuptools.find_packages(),
    # package_dir={'': 'src'},
    # entry_points={
    #     "console_scripts": ['mwjApiTest = mwjApiTest.manage:run']
    # },  # 安装成功后，在命令行输入mwjApiTest 就相当于执行了mwjApiTest.manage.py中的run了
    classifiers=[
        # 'Development Status :: 3 - Alpha',
        # 'Intended Audience :: Developers',
        # 'Topic :: Software Development :: Build Tools',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
