# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     base_soft_assert.py
    Description:   自定义软断言类，支持灵活调用和集成
 -------------------------------------------------
1. 提供基础的断言功能，包括记录、检查和报告断言结果。
2. 支持单独使用或作为上下文管理器使用。
 """

import inspect

import pytest


# from apitesting.src.models import Assertion
# from .logger import logger


class SoftAssert:
    """自定义软断言类，支持灵活调用和集成"""

    def __init__(self):
        self.results_list = []  # 记录所有断言的结果
        self.has_failures = False  # 是否存在失败断言

    def check(self, condition, assert_name=None, error_message="AssertionError: None"):
        """
        记录断言结果。

        :param condition: 表达式或条件，结果应为布尔值
        :param assert_name: 断言名称，默认为None，自动生成
        :param error_message: 如果断言失败时的错误消息
        """
        # 获取调用代码的表达式
        frame = inspect.currentframe().f_back
        code_context = inspect.getframeinfo(frame).code_context
        if code_context:
            expression = code_context[0].strip()
            # print(expression)
            # 提取传入的第一个参数（表达式）
            expression = expression[expression.find("(") + 1: expression.rfind(",", 0)]
            # print(expression)
        else:
            expression = str(condition)

        # 如果断言名称为None，则使用表达式作为断言名称
        # print(type(assert_name))
        assert_info = assert_name or f"{expression}"

        # 执行断言
        try:
            assert condition, error_message
            # 记录成功的断言
            self.results_list.append("✅ " + assert_info)
        except AssertionError as ae:
            # 记录失败的断言
            failure_message = "❌ " + ' | '.join([assert_info, error_message])
            self.results_list.append(failure_message)
            self.has_failures = True  # 标记存在失败断言

    def report(self, clear=True):
        """
        报告所有断言结果。
        "主动调用表示将所有的结果输出"

        :param clear: 是否清空历史结果，默认清空
        :raises AssertionError: 如果有失败断言
        """
        failure_count = len([r for r in self.results_list if r.startswith("❌")])
        success_count = len([r for r in self.results_list if r.startswith("✅")])

        # 报告结果
        report_messages = "\n".join([f"    [{i + 1}] {msg}" for i, msg in enumerate(self.results_list)])
        if clear:
            self.results_list = []  # 清空结果

        if self.has_failures:
            # 使用 pytest.fail 避免过多堆栈信息
            pytest.fail(
                f"Soft Assertion Summary:\n"
                f"{failure_count} failure(s), {success_count} success(es):\n"
                f"{report_messages}",
                pytrace=False,  # 避免输出多余的堆栈信息
            )
        else:
            print(
                f"Soft assertion summary:\n"
                f"{success_count} success(es):\n"
                f"{report_messages}"
            )

    def __enter__(self):
        """进入上下文"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时自动报告断言结果"""
        self.report()
