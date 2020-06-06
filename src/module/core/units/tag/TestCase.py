#! /usr/bin/env python
# -*- coding: UTF-8 -*-
"""
测试用例标签类
"""
import unittest
from enum import Enum, unique


class NewTag:
    def __init__(self, desc=""):
        self.desc = desc


class TestTagDict:
    # Tag 装饰器
    CASE_TAG_FLAG = "__case_tag__"

    # Data 装饰器
    CASE_DATA_FLAG = "__case_data__"

    # unpack 装饰器
    CASE_DATA_UNPACK_FLAG = "__case_data_unpack__"

    # 测试用例真实执行顺序(非跳过)
    CASE_RUN_INDEX_FlAG = "__case_run_index_flag__"

    # 测试用例执行总顺序
    CASE_ID_FLAG = "__case_id__"

    # 测试用例基本函数信息
    CASE_INFO_FLAG = "__case_info__"

    # 跳过标志
    CASE_SKIP_FLAG = "__unittest_skip__"


@unique
class TestParam(Enum):
    ALL = NewTag("完整")  # 完整测试标记，可以重命名，不要删除
    TEST = NewTag("仅测试运行")


def skip(reason):
    """
    跳过用例
    :param reason:
    """

    def wrap(func):
        setattr(func, TestTag.Dict.CASE_SKIP_FLAG, reason)
        return unittest.skip(reason)(func)

    return wrap


def skip_if(condition, reason):
    """
    if条件跳过用例
    :param condition:
    :param reason:
    """

    def wrap(func):
        if condition:
            setattr(func, TestTag.Dict.CASE_SKIP_FLAG, reason)
        return unittest.skipIf(condition, reason)(func)

    return wrap


def tag(*tag_type):
    """
    指定测试用例的标签，可以作为测试用例分组使用，用例默认会有Tag.ALL标签，支持同时设定多个标签，如：
    @tag(Tag.V1_0_0, Tag.SMOKE)
    def test_func(self):
        pass

    :param tag_type:标签类型，在tag.py里边自定义
    """

    def wrap(func):
        if not hasattr(func, TestTag.Dict.CASE_TAG_FLAG):
            tags = {TestTag.Param.ALL}
            tags.update(tag_type)
            setattr(func, TestTag.Dict.CASE_TAG_FLAG, tags)
        else:
            getattr(func, TestTag.Dict.CASE_TAG_FLAG).update(tag_type)
        return func

    return wrap


def data(*values, unpack=True):
    """注入测试数据，可以做为测试用例的数据驱动
    1. 单一参数的测试用例
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        print(box_id)

    2. 多个参数的测试用例
    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)

    3. 是否对测试数据进行解包
    @data({"gold": 1000, "diamond": 100}, {"gold": 2000, "diamond": 200}, unpack=False)
    def test_get_battle_reward(self, reward):
        print(reward)
        print("获得的钻石数量是：{}".format(reward['diamond']))

    :param values:测试数据
    :param unpack: 是否解包
    """

    def wrap(func):
        if hasattr(func, TestTag.Dict.CASE_DATA_FLAG):
            print("\033[0;31;m", "{}的测试数据只能初始化一次".format(func.__name__), "\033[0m")
        else:
            setattr(func, TestTag.Dict.CASE_DATA_FLAG, values)
            setattr(func, TestTag.Dict.CASE_DATA_UNPACK_FLAG, unpack)
        return func

    return wrap


class TestTag:
    """
    测试框架标签
    """

    """
    框架@修饰器
    """
    skip = skip
    skip_if = skip_if
    tag = tag
    data = data
    """
    框架参数
    """
    Param = TestParam
    """
    参数字典
    """
    Dict = TestTagDict
