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

from _hellchin_lib.soft_assert.base_soft_assert import SoftAssert


class BaseMethodAssert:
    """
    BaseMethodAssert 类，用于实现具体的断言方法。硬断言方法。
    """

    def __init__(self, expected_value: Any = None):
        super().__init__()
        self.expected = expected_value

    @staticmethod
    def _parse_assert_data(assert_data: Union[str, dict]) -> dict:
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
        assert_info_fail = f"{assert_info_success} | AssertionError: {fail_message.format(actual=repr(actual), expected=repr(expected))}"
        return assert_info_success, assert_info_fail

    def equal(self, actual, /, expected=None, *, assert_name=None, jsonpath: str = None):
        """
        判断响应相等的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} == {repr(expected)}",
            "expected {actual} to deeply equal {expected} ",
            actual, expected
        )

        assert actual == expected, fail_message

        return success_message

        # 执行断言并记录结果
        # return self.check(actual == expected, success_message, fail_message)

    def not_equal(self, actual, expected=None, assert_name=None, jsonpath: str = None):
        """
        判断响应不相等的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} != {repr(expected)}",
            "expected {actual} not to deeply equal {expected} ",
            actual, expected
        )

        assert actual != expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual != expected, success_message, fail_message)

    def greater_than(self, actual, expected=None, assert_name=None, jsonpath: str = None):
        """
        判断响应大于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} > {repr(expected)}",
            "expected {actual} to be greater than {expected} ",
            actual, expected
        )

        assert actual > expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual > expected, success_message, fail_message)

    def greater_than_or_equal(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        assert actual >= expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual >= expected, success_message, fail_message)

    def greater_than_or_equal_v2(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应值是否大于或等于预期值的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} >= {repr(expected)}",
            "expected {actual} to be greater than or equal to {expected} ",
            actual, expected
        )

        assert actual >= expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual >= expected, success_message, fail_message)

    def less_than(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} < {repr(expected)}",
            "expected {actual} to be less than {expected} ",
            actual, expected
        )

        assert actual < expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual < expected, success_message, fail_message)

    def less_than_or_equal(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断响应小于或等于的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} <= {repr(expected)}",
            "expected {actual} to be less than or equal to {expected} ",
            actual, expected
        )

        assert actual <= expected, fail_message

        return success_message

        # 执行断言并记录结果
        # self.check(actual <= expected, success_message, fail_message)

    def exists(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断 key 是否存在的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} exists",
            "expected {actual} to exist",
            actual, expected
        )

        assert actual in expected, fail_message

        return success_message

    def not_exists(self, actual, expected=None, *, assert_name=None, jsonpath: str = None) -> None:
        """
        判断 key 不存在的逻辑。
        """

        expected = self.expected or expected

        if expected is None:
            raise ValueError("Expected value cannot be None.")

        success_message, fail_message = self._generate_assert_messages(
            assert_name or f"{jsonpath or actual} not exists",
            "expected {actual} to not exist",
            actual, expected
        )

        assert actual not in expected, fail_message

        return success_message


class Expect:
    """
    Expect 类，用于创建一个 to 属性，该属性包含一个 BaseMethodAssert 对象，
    """

    def __init__(self, expected_value: Any):
        self.to = BaseMethodAssert(expected_value)


class PostManAssertMethod:

    def __init__(self):
        self.expect = Expect  # 初始化Expect对象
        self.__success_icon = "✅ "
        self.__failure_icon = "❌ "

    @staticmethod
    def _format_assert_error(desc: str, error_message: str) -> str:
        """
        格式化断言错误信息。
        """
        if desc:
            error_message = error_message.split('|')[1]
            return f"❌ {desc} |{error_message}"
        return f"❌ {error_message}"

    @staticmethod
    def test(desc, test_func=None):
        try:
            # print(f"Running test: {desc}")
            assert_result = test_func()
            print(f"✅ {desc if desc else assert_result}")

        except AssertionError as e:
            # 如果断言失败，我们需要处理下断言信息
            print(PostManAssertMethod._format_assert_error(desc, e.args[0]))

        except Exception as e:
            print("⚠️ Unexpected Error: {}".format(e))


class MethodAssert(SoftAssert):
    def __init__(self, expected_value: Any = None):
        super().__init__()
        self.__base_assert = BaseMethodAssert(expected_value)
        self.expected = expected_value  # 期望值

    def _proxy_method(self, method_name, *args, **kwargs):
        """代理方法，用于调用指定方法并捕获其中的异常"""
        method = getattr(self.__base_assert, method_name)
        try:
            success_result = method(*args, **kwargs)
            self.results_list.append(self.success_icon + success_result)
        except AssertionError as e:
            self.results_list.append(self.failure_icon + e.args[0])

    def __getattr__(self, name):
        """获取属性时自动调用代理方法"""
        if name.startswith('_'):  # 如果方法名以'_'开头，则不进行代理
            pass
        elif hasattr(self.__base_assert, name):
            return lambda *args, **kwargs: self._proxy_method(name, *args, **kwargs)
        else:
            # 如果没有找到指定的方法，则抛出AttributeError异常
            raise AttributeError(f"{type(self).__name__} object has no attribute {name}")


if __name__ == '__main__':
    pm = PostManAssertMethod()
    # pm.expect(1).to.equal(2)
    pm.test("", lambda: pm.expect(1).to.equal(2))
    pm.test("失败断言", lambda: pm.expect(1).to.equal(2))
    pm.test("", lambda: pm.expect(1).to.equal(1))
    pm.test("成功断言", lambda: pm.expect(1).to.equal(1))

    method_assert = MethodAssert()
    method_assert.check(1 == 1)
    method_assert.check(1 == 2)
    method_assert.equal(1, 1)
    method_assert.equal(1, 2)
    method_assert.fail()
