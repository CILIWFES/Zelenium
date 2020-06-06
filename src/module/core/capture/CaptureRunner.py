import time
import threading
from src.module.config import *
from selenium.common.exceptions import NoSuchWindowException


class CaptureRunner(threading.Thread):
    def __init__(self, scheduler, cycle):
        """
        初始化捕捉线程
        :param captureHelper: 图片获取者
        :param scheduler: 调度中心
        :param cycle:     执行周期
        """
        super().__init__()
        self._wait = False
        self._stop = False
        self._cycle = cycle
        self._job_name = scheduler.get_job_name()
        self._sys_logger = scheduler.find_system_logger()
        self._fileHelper = scheduler.find_system_fileHelper()
        self._captureHelper = scheduler.get_CaptureHelper()
        self.path = GF.picture_path(self._job_name)

    def run(self) -> None:
        print("截图线程启动,周期", self._cycle, "秒")

        try:
            times = 1
            while not self._stop:
                try:
                    time.sleep(self._cycle)
                    file_name = "{0}{1}{2}{1}{3}.png".format(self._job_name, GT.SEPARATOR, str(times), int(time.time()))
                    if not self._wait:
                        image = self._captureHelper.screenshot_byte()
                        self._fileHelper.put_queue(self.path, file_name, image)
                    times = times + 1
                except NoSuchWindowException:
                    self._sys_logger.warning("检测到截图窗口切换,截图停止一次")
                    times = times - 1

        except Exception:
            self._sys_logger.error("图片处理线程突然关闭,请确认浏览器非人为关闭")

    def switch_cycle(self, new_cycle):
        """
        切换睡眠周期
        :param new_cycle:
        :return:
        """
        self._cycle = new_cycle

    def stop(self, wait):
        """
        停止并退出线程
        :param wait: 是否等待线程关闭
        :return:
        """
        self._stop = True
        while wait and self.isAlive():
            time.sleep(self._cycle)
            print("图片线程,正在等待结束")

    def wait(self, wait):
        """
        线程设置等待/恢复等待
        :param wait: True为等待,False不等待
        :return:
        """
        self._wait = wait
