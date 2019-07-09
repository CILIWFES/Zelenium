#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from src.code.core.units.tag import *
from .report_tool import report_tool
import unittest


class Meta(type):
    def __new__(cls, clsname, bases, funtions):
        """
        重命名方法值
        :param clsname:
        :param bases:
        :param funtions:
        :return:
        """
        # 筛选出测试用例
        funcs, cases = report_tool.filter_test_case(funtions)

        for test_case in cases.values():
            # 若无装饰器,注入默认用例
            if not hasattr(test_case, TestTag.Dict.CASE_TAG_FLAG):
                setattr(test_case, TestTag.Dict.CASE_TAG_FLAG, {TestTag.Param.ALL})  # 没有指定tag的用例，默认带有tag：ALL

            # 注入测试用例模块名+信息
            case_info = "{}.{}".format(test_case.__module__, test_case.__name__)
            setattr(test_case, TestTag.Dict.CASE_INFO_FLAG, case_info)

            # 过滤不执行的用例
            if not (getattr(test_case, TestTag.Dict.CASE_TAG_FLAG) & set(report_tool.run_case)):
                continue

            # 若有测试数据注入
            if hasattr(test_case, TestTag.Dict.CASE_DATA_FLAG):
                # 根据数据重命名 方法对象
                # 两个数据 执行两次
                funcs.update(report_tool.create_case_with_case_data(test_case))
            else:
                funcs.update(report_tool.create_case_without_case_data(test_case))

        return super(Meta, cls).__new__(cls, clsname, bases, funcs)


class _TestCase(unittest.TestCase, metaclass=Meta):
    def shortDescription(self):
        """覆盖父类的方法，获取函数的注释

        :return:
        """
        doc = self._testMethodDoc
        doc = doc and doc.split()[0].strip() or None
        return doc


def start_patch():
    TestCaseBackup = unittest.TestCase
    unittest.TestCase = _TestCase
    return TestCaseBackup


def stop_patch(TestCaseBackup):
    unittest.TestCase = TestCaseBackup
