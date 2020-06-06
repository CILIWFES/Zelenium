import time
from src.module.config import *
from .ProxyRunner import ProxyRunner
from browsermobproxy import Server, Client


class ProxyHelper:
    def __init__(self, scheduler, proxy):
        self._scheduler = scheduler
        self._proxy: Client = proxy
        self._proxyRunner: ProxyRunner = None
        self._job_name = self._scheduler.get_job_name()
        self._memory_dict = {}
        self._history = {}
        self._memory_point = None

    def get_respone(self, start=None, end=None):
        """
        获取[start,end) 区间内的请求
        :param start:
        :param end:
        :return:
        """
        lenght = len(self._proxy.har['log']['entries'])
        if end is None and start is None:
            return self._proxy.har['log']['entries']
        elif end is None and start is not None and start < lenght:
            return self._proxy.har['log']['entries'][start:]
        elif end is not None and start is None and end <= lenght:
            return self._proxy.har['log']['entries'][0:end]
        elif end is not None and start is not None and start < lenght and end <= lenght:
            return self._proxy.har['log']['entries'][start:end]
        else:
            return []

    def wait_response(self, url, times=None, wait_time=0.5):
        """
        等待url的响应,获取url的返回值
        :return: (request,response)
        """
        assert self._memory_point is not None, "请设立记忆点"
        isContinue = True
        nowTimes = 1
        nowIndex = self._memory_point

        while isContinue:
            hars = self.get_respone(start=nowIndex)

            for item in hars:
                url_item: str = self.get_dict_data(item, ('request', 'url'))
                if url_item.find(url) >= 0:
                    return item
            nowIndex += len(hars)

            if times is not None:
                isContinue = False if nowTimes >= times else True
                nowTimes += 1
            time.sleep(wait_time)

    def set_memory_point(self):
        """
        记录下一个har的坐标
        :return:
        """
        self._memory_point = len(self._proxy.har['log']['entries'])

    def get_memory_data(self, start=None, end=None, url=None):
        """
        获取记忆点之间的包,可通过url过滤
        :param start: 起始记忆
        :param end:   终止记忆
        :param url:   过滤条件
        :return:
        """
        assert start is not None or end is not None, "请输入一个记忆点"
        startIndex = self._memory_dict[start] if start is not None else None
        endIndex = self._memory_dict[end] if end is not None else None
        respones_data = self.get_respone(startIndex, endIndex)
        respones = []
        if url is not None:
            for item in respones_data:
                url_item: str = self.get_dict_data(item, ('request', 'url'))
                if url_item.find(url) >= 0:
                    respones.append(item)
        else:
            respones = respones_data
        return respones

    def get_response_data(self, entry):
        """
        通过response,获取其间的数据
        :param response: 响应文件
        :return: dict
        """
        pass

    def get_request_data(self, entry):
        """
        request,获取其间的数据
        :param request: 请求文件
        :return: dict
        """
        pass

    def set_point(self, name):
        """
        设置记忆点
        :return: 返回值 dict
        """

        # 设置下一个包的index
        self._memory_dict[name] = len(self._proxy.har['log']['entries'])


    def get_error(self, start_name=None, end_name=None):
        """
        获取记忆点之间的错误request,response
        :param start_name:  起始记忆点名字
        :param end_name: 终止记忆点名字
        :return: (request,response)
        """
        pass

    def runner_start(self, jump_rule=False, cycle=None):
        """
        启动线程
        :param jump_rule:
        :param cycle: 线程运行周期
        :return:
        """
        if self.runner_alive():
            return True

        if cycle is None:
            cycle = float(GF.get_config(GT.PROXY_CYCLE))

        self._proxyRunner = ProxyRunner(self._scheduler, jump_rule, cycle)

        # 是否开启线程记录
        self._proxyRunner.start()

    def runner_alive(self):
        """
        判断线程存活
        :return:
        """
        if self._proxyRunner is None:
            return False

        return self._proxyRunner.isAlive()

    def runner_wait(self, wait):
        """
        判断线程暂停
        :param wait:
        :return:
        """
        if self._proxyRunner is None:
            return False

        self._proxyRunner.wait(wait)

    def runner_stop(self, wait=True):
        """
        是否等待,默认阻塞等待线程终止
        :param wait:
        :return:
        """
        if self._proxyRunner is None:
            return True

        self._proxyRunner.stop(wait)

    def runner_cycle(self, new_cycle):
        """
        切换线程睡眠周期
        :param new_cycle:
        :return:
        """
        if self._proxyRunner is None:
            return False

        self._proxyRunner.switch_cycle(new_cycle)

    def get_dict_data(self, result, paths: tuple):
        """
        获取字典下的路径
        :param result:
        :param paths:
        :return:
        """
        data = result
        for item in paths:
            if item in data:
                data = data[item]
            else:
                return None
        return data
