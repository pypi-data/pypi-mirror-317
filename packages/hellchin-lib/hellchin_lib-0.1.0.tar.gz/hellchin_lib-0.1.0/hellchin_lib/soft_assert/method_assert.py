# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     method_assert.py
    Description:   具体断言逻辑实现
 -------------------------------------------------

 继承 SoftAssert 类，扩展出具体的断言方法。
 如 equal、not_equal、greater_than 等。
 """

from typing import Union, Any

# from .logger import logger
from .base_soft_assert import SoftAssert


# from apitesting.src.models import Assertion


class MethodAssert(SoftAssert):
    """类型为json的响应断言，封装各种断言方法"""

    # # 支持的运算符列表，优先匹配长度较长的运算符
    # SUPPORTED_OPERATORS = ["not in", "in", ">=", "<=", "!=", "==", ">", "<"]

    # def __init__(self, response_json: dict, assert_data):
    #     """
    #     :param response_json: 响应的json数据
    #     :param assert_data: 断言数据, 可以是字符串或者AssertData对象
    #     """
    #     super().__init__()  # 初始化 SoftAssert
    #     self.response_json = response_json
    #     self.assert_data = self._parse_assert_data(assert_data)
    #
    #     self.actual_value = json_handler.jsonpath_query(self.response_json, self.assert_data.jsonpath)[0]
    #     self.jsonpath_expression = self.assert_data.jsonpath  # 获取断言的jsonpath表达式
    #     self.assert_name = self.assert_data.name  # 获取断言名称
    #     self.expected_value = self.assert_data.value  # 获取断言的预期值

    def _parse_assert_data(self, assert_data: Union[str, dict]) -> dict:
        """
        解析断言数据，支持字符串或 pydantic 模型

        :param assert_data: 可能是字符串表达式或 pydantic 模型
        :return: 解析后的 Assertion 对象
        """
        if isinstance(assert_data, dict):  # Assertion
            return assert_data
        elif isinstance(assert_data, str):
            # 解析字符串格式，比如 `$.code > "200"`
            # return self._parse_string_assert(assert_data)
            raise ValueError(f"Unsupported assert_data type: {type(assert_data)}")
        else:
            raise ValueError(f"Unsupported assert_data type: {type(assert_data)}")

    @staticmethod
    def _generate_assert_messages(success_condition: str, fail_message: str, actual, expected) -> tuple:
        """
        生成断言的成功和失败信息。

        :param success_condition: 成功条件描述
        :param fail_message: 失败消息模板
        :param actual: 实际值
        :param expected: 预期值
        :return: 成功信息和失败信息
        """
        assert_info_success = success_condition
        assert_info_fail = f"AssertionError: {fail_message.format(actual=repr(actual), expected=repr(expected))}"
        return assert_info_success, assert_info_fail

    def equal(self, actual, expected, assert_name=None, jsonpath: str = None):
        """
        判断响应相等的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} == {repr(expected)}",
            "expected {actual} to deeply equal {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual == expected, success_message, fail_message)

    def not_equal(self, actual, expected, assert_name=None, jsonpath: str = None):
        """
        判断响应不相等的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} != {repr(expected)}",
            "expected {actual} not to deeply equal {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual != expected, success_message, fail_message)

    def greater_than(self, actual, expected, assert_name=None, jsonpath: str = None):
        """
        判断响应大于的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} > {repr(expected)}",
            "expected {actual} to be greater than {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual > expected, success_message, fail_message)

    def greater_than_or_equal(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual >= expected, success_message, fail_message)

    def greater_than_or_equal_v2(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual >= expected, success_message, fail_message)

    def less_than(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} < {repr(expected)}",
            "expected {actual} to be less than {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual < expected, success_message, fail_message)

    def less_than_or_equal(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于或等于的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} <= {repr(expected)}",
            "expected {actual} to be less than or equal to {expected} ",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual <= expected, success_message, fail_message)

    def exists(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断 key 是否存在的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} exists",
            "expected {actual} to exist",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual == expected, success_message, fail_message)

    def not_exists(self, actual, expected, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断 key 不存在的逻辑。
        """

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} not exists",
            "expected {actual} to not exist",
            actual, expected
        )

        # 执行断言并记录结果
        self.check(actual != expected, success_message, fail_message)
