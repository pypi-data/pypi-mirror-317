# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     setup.py
    Description:   包的元信息
 -------------------------------------------------
 """
from pathlib import Path

from setuptools import setup, find_packages

setup(
    name="hellchin_lib",     # 包名
    version="0.1.2",     # 版本号
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
    # long_description=(Path("README.md").read_text() + "\n\n" + Path("CHANGELOG.md").read_text()),
    # long_description_content_type="text/markdown",
)
