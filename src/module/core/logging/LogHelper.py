import logging
from src.module.config import *
from src.module.tools import file_tools


class LogHelper(logging.Logger):
    msg_position = '-msg:'

    def __init__(self, job_name, file_name):
        """
        日志文件类
        :param job_name:
        :param suffix:
        """
        self._job_name = job_name
        self._file_name = file_name
        super().__init__(job_name)

        self.setLevel(logging.INFO)
        # 日志格式设置
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s ' + LogHelper.msg_position + ' %(message)s')

    def add_FileHandler(self):
        """
        写入日志文件
        :return:
        """
        path = GF.log_path(self._job_name)

        file_tools.create_dir(path)
        file_handler = logging.FileHandler(path + self._file_name, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(self.formatter)
        self.addHandler(file_handler)

    def add_ConsoleHandler(self):
        """
        控制台日志显示
        :return:
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(self.formatter)

        self.addHandler(console_handler)
