import time
import queue
from src.code.config import *
from src.code.core.file.FileRunner import FileRunner


class FileHelper:
    def __init__(self, scheduler, cycle=None, runner_size=None, maxsize=None):
        """
        初始文件线程池
        :param scheduler: 调度模型
        :param cycle:     睡眠周期
        :param runner_size: 线程数
        :param maxsize:     最大队列长度
        """
        super().__init__()
        self._stop = False
        self._wait = False
        # 线程池
        self._fileRunners: list = []
        # 调度中心
        self._scheduler = scheduler
        # 文件线程
        maxsize = int(GF.get_config(GT.FILE_QUEUE_SIZE)) if maxsize is None else maxsize
        # 工作队列
        self._working_queue = queue.Queue(maxsize)
        # 周期
        self._cycle = float(GF.get_config(GT.FILERUNNER_CYCLE)) if cycle is None else cycle

        self._runner_size = int(GF.get_config(GT.FILERUNNER_COUNT)) if runner_size is None else runner_size

    def pop_queue(self):
        """
        从队列中获取元素
        :return:
        """
        path, fileName, content = self._working_queue.get()
        return path, fileName, content

    def put_queue(self, path, file_name, content):
        """
        外部插入元素,执行队列
        :param path:
        :param file_name:
        :param content:
        :return:
        """
        self._working_queue.put((path, file_name, content))
        return True

    def runner_start(self):
        """
        开启文件线程
        :return:
        """
        assert self.runner_status()[0] == 0, "线程已启动"
        self._fileRunners = [FileRunner(self) for i in range(self._runner_size)]
        for item in self._fileRunners:
            item.start()

    def runner_wait(self, wait):
        """
        所有线程等待
        :return:
        """
        assert self._fileRunners is not None and len(self._fileRunners) > 0, "线程未启动"

        for item in self._fileRunners:
            item.wait(wait)

    def runner_stop(self, wait=True):
        """
        停止线程
        :param wait:
        :return:
        """
        assert self._fileRunners is not None and len(self._fileRunners) > 0, "线程未启动"
        for item in self._fileRunners:
            item.wait(False)
            item.stop()
        while wait and self.runner_status()[0] == 0:
            time.sleep(self._cycle)

    def runner_status(self):
        """
        检查线程状态
        :return:
        """
        isAlive = 0
        isStop = 0
        for item in self._fileRunners:
            if item.isAlive():
                isAlive += 1
            else:
                isStop += 1

        return isAlive, isStop

    def get_runner_size(self):
        """
        获取线程数
        :return:
        """
        return len(self._fileRunners)

    def get_cycle(self):
        """
        睡眠周期
        :return:
        """
        return self._cycle

    def get_job_name(self):
        """
        任务名字
        :return:
        """
        return self._scheduler.get_job_name()
