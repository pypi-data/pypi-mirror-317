# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 -------------------------------------------------
    File Name:     test_assertions.py
    Description:   测试代码
 -------------------------------------------------
 """

from hellchin_lib.soft_assert.method_assert import MethodAssert


def test_soft_assert_method():
    method_assert = MethodAssert()

    with method_assert:
        method_assert.equal(1, 1, "Check if 1 equals 1")
        method_assert.not_equal(1, 2, "Check if 1 does not equal 2")
        method_assert.greater_than(5, 3, "Check if 5 is greater than 3")
        # method_assert.equal(1, 2, "This will fail")  # 故意失败


def test_soft_assert():
    method_assert = MethodAssert()
    # 1. 直接调用方法断言的方法，手动输出断言结果
    method_assert.equal(1, 1, assert_name="test")
    method_assert.not_equal(1, "2", jsonpath="$.a")
    # method_assert.check(1 == 3)
    method_assert.report()  # 调用方法断言的report方法，输出断言结果


if __name__ == '__main__':
    test_soft_assert()
