# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     setup.py
    Description:   包的元信息
 -------------------------------------------------
 """
from setuptools import setup, find_packages

setup(
    name="hellchin_lib",     # 包名
    version="0.1.0",     # 版本号
    description="A Python library for soft assertions and flexible testing.",   # 描述
    author="hellchin",     # 作者
    author_email="your.email@example.com",  # 作者邮箱
    packages=find_packages(),   # 包列表: 自动查找所有包含__init__.py文件的目录
    install_requires=[
        "pytest>=6.0.0",    # 依赖的包
    ],
    classifiers=[   # 分类器列表
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
