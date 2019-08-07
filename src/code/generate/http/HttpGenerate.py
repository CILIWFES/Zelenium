from src.code.config import *
from src.code.tools import *
from src.code.core.logging.LogHelper import LogHelper


class HttpGenerate:
    def __init__(self, job_name, suffix='_proxy.txt'):
        self._job_name = job_name
        self._file_name = job_name + suffix
        self._path = GF.log_path(self._job_name)
        self._package = []
        self.__decode()
        self.msg_position = LogHelper.msg_position

    def __decode(self):
        """
        将日志转化为字典
        :return:
        """
        assert file_tools.exist(self._path + self._file_name), "文件不存在"
        contents = file_tools.read_file_line(self._path, self._file_name)
        for content in contents:
            index = content.find(self.msg_position)
            if index == -1:
                continue
            else:
                item = eval(content[index + len(self.msg_position):])
            self._package.append(item)

    def generate(self):

        return
