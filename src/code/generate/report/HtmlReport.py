from src.code.config import *
from src.code.core.units.tag import *
from src.code.tools.file.FileTools import file_tools
from src.code.generate.report.tag_report import *
import os


class ReportTools:

    def generate(self, job_name, run_dir, run_tags=None, report_title="自动化测试报告"):
        """
        生成Html测试报告
        :param job_name:任务名字
        :param run_dir: 执行的相对文件目录
        :param run_tags: 运行案例
        :param report_title: 报告标题
        """
        if run_tags is None:
            run_tags = {TestTag.Param.ALL}

        run_dir = GT.SYS_ROOT_PATH + run_dir
        report_tool.run_case = run_tags
        # 生成测试调度类
        runner = TestStarter(job_name)
        # 添加例子扫描路径
        runner.add_case_dir(run_dir)
        # 执行测试
        open_path = runner.run_test(report_title=report_title)
        # 文件存在,默认打开报告
        if file_tools.exist(open_path):
            cmd = open_path
            cmd = cmd.replace('/', '\\')
            os.system('explorer.exe /e,' + cmd)


html_report = ReportTools()
