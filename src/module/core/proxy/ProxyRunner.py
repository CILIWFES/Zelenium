import time
import threading
from src.module.config import *


class ProxyRunner(threading.Thread):
    def __init__(self, scheduler, jump_rule, cycle):
        """
        初始化捕捉线程
        :param scheduler: 调度中心
        :param jump_rule: 是否进行规则检查,True 跳过 False 执行规则检查
        :param scheduler: 调度中心
        :param cycle:     执行周期
        """
        super().__init__()
        self._wait = False
        self._stop = False
        self._cycle = cycle
        self._jump_rule = jump_rule
        self._job_name = scheduler.get_job_name()
        self._proxyHelper = scheduler.get_ProxyHelper()
        self._sys_logger = scheduler.find_system_logger()
        self._proxy_logger = scheduler.find_proxy_logger()

        # 执行过的坐标
        self._search_index = 0

    def run(self) -> None:
        print("代理线程启动,周期", self._cycle, "秒")
        self._proxy_logger.info("代理线程启动,周期" + str(self._cycle) + "秒")
        times = 1
        while not self._stop:
            time.sleep(self._cycle)
            if not self._wait:
                # 获取新的请求
                results: list = self._proxyHelper.get_respone(start=self._search_index)
                if results is not None and len(results) > 0:
                    self._search_index += len(results)
                    # 是否跳过规则
                    if self._jump_rule:
                        # 直接保存
                        for result in results:
                            self._logger(result)
                    else:
                        # 执行规则检查保存
                        self._monitor(results)

            times = times + 1

    def _monitor(self, results: list):
        """
        监视路由请求,解析并记录
        :param results:
        :return:
        """
        for result in results:
            islog = self._check_rule(result)
            if islog:
                self._logger(result)

    def _logger(self, result):
        """
        将请求保存至日志
        :param result:
        :return:
        """
        if result['response']['status'] != 200:
            self._proxy_logger.error(result)
        else:
            self._proxy_logger.info(result)

    def _check_rule(self, result):
        mimeType: str = self._proxyHelper.get_dict_data(result, ('response', 'content', 'mimeType'))
        methed: str = self._proxyHelper.get_dict_data(result, ('request', 'method'))
        text: str = self._proxyHelper.get_dict_data(result, ('response', 'content', 'text'))

        # 非空判断
        if mimeType is None and methed is None:
            return False

        # 过滤请求返回类型
        if mimeType.find('application/json') >= 0 or mimeType.find('text/html') >= 0:
            # 过滤界面
            if methed.find("GET") >= 0 and mimeType.find('text/html') >= 0 and text is not None and text.find(
                    "DOCTYPE") >= 0:
                return False
            return True
        else:
            return False



    def switch_cycle(self, new_cycle):
        """
        切换睡眠周期
        :param new_cycle:
        :return:
        """
        self._cycle = new_cycle

    def stop(self, wait):
        """
        终止线程
        :param wait: 是否等待
        :return:
        """
        self._stop = True
        while wait and self.isAlive():
            time.sleep(self._cycle)
            print("图片线程,正在等待结束")

    def wait(self, wait):
        """
        线程等待
        :param wait: True 等待,False 不等待
        :return:
        """
        self._wait = wait
