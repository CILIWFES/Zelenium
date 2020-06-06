#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import os
import io
import datetime
import sys
from .report_core import *
from src.module.config import *
from src.module.core.scheduler import *
from src.module.tools import file_tools
from .report_tool import report_tool
from .template import report_style_1
from .template import report_style_2


class _TestResult(unittest.TestResult):
    def __init__(self, verbosity=1):
        super().__init__(verbosity)
        self.outputBuffer = io.StringIO()
        self.raw_stdout = None
        self.raw_stderr = None
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.verbosity = verbosity
        self.result = []
        self._case_start_time = 0
        self._case_run_time = 0

    def startTest(self, test):
        """
        启动测试
        :param test:
        :return:
        """
        # 记录时间
        self._case_start_time = time.time()
        # 开始执行
        super().startTest(test)
        # 切换控制台
        self.raw_stdout = sys.stdout
        self.raw_stderr = sys.stderr
        # 输入流
        sys.stdout = self.outputBuffer
        sys.stderr = self.outputBuffer

    def complete_output(self):
        """
        完成输出后,切回系统打印,返回测试结果
        :return:
        """

        # 计算时间
        self._case_run_time = time.time() - self._case_start_time

        # 切回系统打印
        if self.raw_stdout:
            sys.stdout = self.raw_stdout
            sys.stderr = self.raw_stderr

        # 获取输出流结果
        result = self.outputBuffer.getvalue()
        self.outputBuffer.seek(0)
        self.outputBuffer.truncate()

        # 打印日志
        if result and GF.show_print_in_console():
            scheduler.show_console(result.strip())

        return result

    def stopTest(self, test):
        """
        测试结束,执行
        :param test:
        :return:
        """
        self.complete_output()

    def addSuccess(self, test):
        """
        测试用例执行成功
        :param test:
        :return:
        """
        self.success_count += 1
        super().addSuccess(test)
        output = self.complete_output()
        # 添加测试结果(结果标识,方法,错误日志,输出,执行时间)
        self.result.append((0, test, output, '', self._case_run_time))

    def addError(self, test, err):
        """
        当测试用例错误
        :param test:
        :param err:
        :return:
        """
        self.error_count += 1
        super().addError(test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str, self._case_run_time))

        # 打印出错日志
        scheduler.show_console('TestCase Error', 'E')
        if GF.show_error_traceback():
            scheduler.show_console(_exc_str, 'E')

    def addSkip(self, test, reason):
        """
        测试用例跳过
        :param test:
        :param reason:
        :return:
        """
        self.skip_count += 1
        super().addSkip(test, reason)
        self.result.append((3, test, "", "", 0.0))

    def addFailure(self, test, err):
        """
        测试用例失败
        :param test:
        :param err:
        :return:
        """
        self.failure_count += 1
        super().addFailure(test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str, self._case_run_time))

        # 打印错误日志
        scheduler.show_console('TestCase Failed', 'E')
        if GF.show_error_traceback():
            scheduler.show_console(_exc_str, 'E')


class TestRunner:
    STATUS = {
        0: '通过',
        1: '失败',
        2: '异常',
        3: '跳过',
    }

    def __init__(self, job_name, report_title, report_dir, verbosity=1, description=""):
        self._job_name = job_name
        self.report_dir = report_dir
        self.verbosity = verbosity
        self.title = report_title
        self.description = description
        self.start_time = datetime.datetime.now()
        self.stop_time = None

        self.result_data = dict()
        self.result_data['testResult'] = []

    def run(self, test):
        msg = "开始测试，用例数量总共{}个，跳过{}个，实际运行{}个"
        scheduler.show_console(msg.format(report_tool.total_case_num,
                                          report_tool.total_case_num - report_tool.actual_case_num,
                                          report_tool.actual_case_num), "I")
        result = _TestResult(self.verbosity)
        test(result)
        self.stop_time = datetime.datetime.now()
        # 解析数据
        self.analyze_test_result(result)
        scheduler.show_console('时间 花费: {}'.format(self.stop_time - self.start_time), "I")

        if GF.create_report(1):
            file_path = os.path.join(self.report_dir,
                                     f"{self._job_name}-{self.start_time.strftime('%Y-%m-%d-%H-%M-%S')}-报告1.html")
            report_style_1.build_report(file_path, self.result_data)

        if GF.create_report(2):
            file_path = os.path.join(self.report_dir,
                                     f"{self._job_name}-{self.start_time.strftime('%Y-%m-%d-%H-%M-%S')}-报告2.html")
            report_style_2.build_report(file_path, self.result_data)

        return self.report_dir

    def sort_result(self, case_results):
        """
        python3.6 dict特性转化为排序列表
        :param case_results:
        :return:
        """
        rmap = {}
        classes = []
        for n, t, o, e, run_time in case_results:
            cls = t.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append((n, t, o, e, run_time))
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    def analyze_test_result(self, result):
        """
        分析用例报告,返回测试结果
        :param result:
        :return:
        """
        self.result_data["reportName"] = self.title
        self.result_data["beginTime"] = str(self.start_time)[:19]
        self.result_data["totalTime"] = str(self.stop_time - self.start_time)
        # 转化为排序列表
        sorted_result = self.sort_result(result.result)

        for cid, (cls, cls_results) in enumerate(sorted_result):
            pass_num = fail_num = error_num = skip_num = 0
            name = "{}.{}".format(cls.__module__, cls.__name__)
            current_class_name = name
            for tid, (state_id, t, o, e, run_time) in enumerate(cls_results):
                # 统计
                if state_id == 0:
                    pass_num += 1
                elif state_id == 1:
                    fail_num += 1
                elif state_id == 2:
                    error_num += 1
                else:
                    skip_num += 1

                name = t.id().split('.')[-1]
                # 获取函数文档注释
                doc = t.shortDescription() or ""
                case_data = dict()
                case_data['className'] = current_class_name
                case_data['methodName'] = name
                case_data['spendTime'] = "{:.2}S".format(run_time)
                case_data['description'] = doc
                case_data['log'] = o + e

                case_data['status'] = self.STATUS[state_id]
                self.result_data['testResult'].append(case_data)

        self.result_data["testPass"] = result.success_count
        self.result_data[
            "testAll"] = result.success_count + result.failure_count + result.error_count + result.skip_count
        self.result_data["testFail"] = result.failure_count
        self.result_data["testSkip"] = result.skip_count
        self.result_data["testError"] = result.error_count


class TestStarter:

    def __init__(self, job_name):
        self._job_name = job_name
        self.__TestCaseBackup = start_patch()
        self.case_dirs = []

    def add_case_dir(self, dir_path):
        """
        添加测试用例文件夹，多次调用可以添加多个文件夹，会按照文件夹的添加顺序执行用例
            runner = TestRunner()
            runner.add_case_dir(r"testcase\chat")
            runner.add_case_dir(r"testcase\battle")
            runner.run_test(report_title='接口自动化测试报告')

        :param dir_path:
        :return:
        """
        if not os.path.exists(dir_path):
            raise Exception("测试用例文件夹不存在：{}".format(dir_path))

        if dir_path in self.case_dirs:
            scheduler.show_console("测试用例文件夹已经存在了：{}".format(dir_path), "W")
        else:
            self.case_dirs.append(dir_path)

    def run_test(self, report_title='接口自动化测试报告'):
        """
        执行测试
        :param report_title:
        :return:
        """
        path = GF.html_path(self._job_name)

        if not self.case_dirs:
            raise Exception("请先调用add_case_dir方法，添加测试用例文件夹")

        file_tools.create_dir(path)

        report_dir = os.path.abspath(path)

        suite = unittest.TestSuite()
        """扫描测试路径"""
        for case_path in self.case_dirs:
            suite.addTests(unittest.TestLoader().discover(case_path))
        opne_path = TestRunner(self._job_name, report_dir=report_dir, report_title=report_title).run(suite)
        stop_patch(self.__TestCaseBackup)
        return opne_path
