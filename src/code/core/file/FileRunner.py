import time
import threading
from src.code.tools import file_tools


class FileRunner(threading.Thread):
    def __init__(self, fileHelper):
        super().__init__()
        self._job_name = fileHelper.get_job_name()
        # 等待状态
        self._wait = False
        # 暂停状态
        self._stop = False
        # 执行周期
        self._cycle = fileHelper.get_cycle()
        # 文件调度类
        self._fileHelper = fileHelper

    def run(self):
        while not self._stop:
            if not self._wait:
                self.execution()
            time.sleep(self._cycle)

    def execution(self):
        """
        从文件队列取出元素,并保存
        :return:
        """
        path, file_name, content = self._fileHelper.pop_queue()
        file_tools.save_file(path, file_name, content)

    def stop(self):
        """
        停止线程的运行
        :return:
        """
        self._stop = True

    def wait(self, wait):
        """
        线程设置等待
        :param wait: True 为等待,False 不等待
        :return:
        """
        self._wait = wait
