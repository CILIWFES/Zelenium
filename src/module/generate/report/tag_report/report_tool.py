import functools
import time
from src.module.config import *
from src.module.core import *
from src.module.core.units.tag import *


class ReportTool:
    def __init__(self):
        self.run_case: set = None
        self.actual_case_num = 0
        self.total_case_num = 0

    def create_case_id(self):
        """
        执行用例数的累加
        :return:
        """
        self.total_case_num += 1
        return self.total_case_num

    def create_actual_run_index(self):
        """
        返回实际运行数的累加
        :return:
        """
        self.actual_case_num += 1
        return self.actual_case_num

    def modify_func_name(self, func):
        """
        修改函数名字，实现unittest框架的排序
        例如: test_fight ---> test_00001_fight
        :param func:
        :return:
        """
        case_id = self.create_case_id()
        # 添加成员变量
        setattr(func, TestTag.Dict.CASE_ID_FLAG, case_id)

        # 重命名函数
        func_name = func.__name__.replace("test_", "test_{:05d}_".format(case_id))

        return func_name

    def append_name_with_test_data(self, func_name, index, test_data):
        """
        根据使用的数据逆序拼接至函数名
        :param func_name:
        :param index:
        :param test_data:
        :return:
        """
        params_str = "_".join([str(_) for _ in test_data]).replace(".", "")
        # 逆序拼接
        func_name += "_{:05d}_{}".format(index, params_str)
        if len(func_name) >= 80:
            func_name = func_name[0:80] + "..."
        return func_name

    def create_case_with_case_data(self, func):
        """
        创建包含数据的例子
        :param func:
        :return:
        """
        result = dict()
        # 遍历测试数据
        # index初始为1,test_data为数据
        for index, test_data in enumerate(getattr(func, TestTag.Dict.CASE_DATA_FLAG), 1):
            if not hasattr(func, TestTag.Dict.CASE_SKIP_FLAG):
                # 未跳过,注入执行顺序
                setattr(func, TestTag.Dict.CASE_RUN_INDEX_FlAG, self.create_actual_run_index())

            # 名字重排
            func_name = self.modify_func_name(func)

            # 通过类型来设置参数
            if isinstance(test_data, list):
                # 新函数名=函数名_数据
                func_name = self.append_name_with_test_data(func_name, index, test_data)

                if getattr(func, TestTag.Dict.CASE_DATA_UNPACK_FLAG, None):
                    result[func_name] = _handler(_feed_data(*test_data)(func))
                else:
                    result[func_name] = _handler(_feed_data(test_data)(func))

            elif isinstance(test_data, dict):
                # 新函数名=函数名_数据
                func_name = self.append_name_with_test_data(func_name, index, test_data.values())

                if getattr(func, TestTag.Dict.CASE_DATA_UNPACK_FLAG, None):
                    result[func_name] = _handler(_feed_data(**test_data)(func))
                else:
                    result[func_name] = _handler(_feed_data(test_data)(func))

            elif isinstance(test_data, (int, str, bool, float)):
                # 新函数名=函数名_数据
                func_name = self.append_name_with_test_data(func_name, index, [test_data])
                result[func_name] = _handler(_feed_data(test_data)(func))

            else:
                raise Exception("无法解析{}".format(test_data))

        return result

    def create_case_without_case_data(self, func):
        """
        创建无数据用例
        :param func:
        :return:
        """
        if not hasattr(func, TestTag.Dict.CASE_SKIP_FLAG):
            setattr(func, TestTag.Dict.CASE_RUN_INDEX_FlAG, self.create_actual_run_index())

        result = dict()
        func_name = self.modify_func_name(func)

        result[func_name] = _handler(func)
        return result

    def filter_test_case(self, funcs_dict):
        """
        过滤方法列表筛选出测试用例,功能
        :param funcs_dict:
        :return:
        """
        funcs = dict()
        cases = dict()
        for i in funcs_dict:
            if i.startswith("test_"):
                cases[i] = funcs_dict[i]
            else:
                funcs[i] = funcs_dict[i]

        return funcs, cases


report_tool = ReportTool()


def _handler(func):
    """
    函数代理
    :param func:
    :return:
    """

    # functools.wraps 是运行时复制原始函数信息
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        time.sleep(GF.report_execute_interval())
        msg = "start to test {} ({}/{})".format(getattr(func, TestTag.Dict.CASE_INFO_FLAG),
                                                getattr(func, TestTag.Dict.CASE_RUN_INDEX_FlAG),
                                                report_tool.actual_case_num)
        scheduler.show_console(msg, "I")
        result = func(*args, **kwargs)
        return result

    return wrap


def _feed_data(*args, **kwargs):
    """
    运行时注入参数
    :param args:
    :param kwargs:
    :return:
    """

    def wrap(func):
        # functools.wraps 是运行时复制原始函数信息
        @functools.wraps(func)
        def _wrap(self):
            return func(self, *args, **kwargs)

        return _wrap

    return wrap
