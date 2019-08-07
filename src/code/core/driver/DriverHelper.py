import time
from src.code.config import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver as ChromiumDriver


class DriverHelper(ChromiumDriver):
    """
    继承谷歌浏览器类
    """
    # 防止无限等待,设置等待展示时间,默认20秒
    show_print_time = 20

    # 初始打开谷歌浏览器
    def __init__(self, job_name, options, windows_size=1, headless=False, mute=False, image=True):
        """
        初始化浏览器句柄
        :param job_name:    任务名称
        :param options:     浏览器初始化选项
        :param headless:    禁默开关
        :param mute:        静音开关
        :param image:       显示图像开关
        """

        """---任务名称---"""
        self.job_name = job_name

        """记忆窗口缓存字典"""
        self.memory_windows = {}

        """---前处理---"""

        """根据输入的参数,获取装配好的选项"""
        options = self.__prepare_befor(options, headless, mute, image)

        """调用谷歌浏览器(父类)初始化,获取句柄"""
        super().__init__(GF.chrom_path(), options=options)

        """---后处理---"""

        """设置浏览器界面,开启截屏与日志"""
        self.__prepare_after(windows_size)

        self._memory_cookies = {}

    def __prepare_befor(self, options, headless, mute, image):
        """
        基础配置
        :param options: 浏览器初始化选项
        :param headless: 禁默开关
        :param mute: 静音开关
        :param image: 显示图像开关
        :return: options 浏览器初始化选项
        """
        # 设置配置
        if options is None:
            options = webdriver.ChromeOptions()
        # 静音启动
        if mute:
            options.add_argument("--mute-audio")

        # 加载图片
        if not image:
            # 禁止加载图片
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

        # 禁默启动
        if headless:
            options.add_argument('headless')
            # 无头模式,屏幕大小只能手动设置
            size = GF.headless_windows_size()
            options.add_argument('window-size=' + str(size[0]) + ',' + str(size[1]))

        return options

    def __prepare_after(self, windows_size):
        """
        处理屏幕设置
        :param windows_size:
        :return:
        """
        if windows_size is None:
            self.maximize_window()

        elif isinstance(windows_size, int):
            if windows_size == 0:
                self.minimize_window()
            elif windows_size == 1:
                self.maximize_window()
            else:
                raise Exception("错误windows_size标志,无效数字:", windows_size)

        elif isinstance(windows_size, (tuple, list)):
            self.set_window_size(windows_size[0], windows_size[1])

        else:
            raise Exception("错误windows_size标志")

    def wait_show(self, search_xpath, times=None, wait_time=1):
        """
        在一定时间内等待Xpath元素出现
        :param search_xpath: 等待的xpath路径
        :param times: 等待次数,超出即报错,None为永久等待
        :param wait_time: 每次等待时间
        :return:出现返回True,未出现返回False
        """
        isContinue = True
        nowTimes = 1
        total_wait = 0

        # 开始等待
        while isContinue:
            if self.exist_xpath(search_xpath):
                return True
            elif times is not None:
                isContinue = False if nowTimes >= times else True
            time.sleep(wait_time)

            # 防止无限等待,没有反馈
            if total_wait >= self.show_print_time:
                print("注意! 等待节点:", search_xpath, "超过", self.show_print_time, "秒")
                total_wait -= self.show_print_time
            else:
                total_wait += wait_time

            # 当前次数累加
            nowTimes += 1

        return False

    def get_node_available(self, xpath, times=20, wait_time=0.5):
        """
        等待元素出现,并获取元素,默认等待10秒
        :param wait_time:
        :param times:
        :param xpath:
        :return:
        """
        if not self.wait_show(xpath, times, wait_time):
            raise Exception("等待节点:", xpath, "超时")

        return self.find_element_by_xpath(xpath)

    def get_nodes_available(self, xpath, times=20, wait_time=0.5):
        """
        等待元素出现,并获取元素,默认等待20秒
        :param wait_time:
        :param times:
        :param xpath:
        :return:
        """
        if not self.wait_show(xpath, times, wait_time):
            raise Exception("等待节点超时")

        return self.find_elements_by_xpath(xpath)

    # 关闭谷歌浏览器
    def quit(self):
        """
        简单的关闭谷歌浏览器
        :return:
        """
        super().quit()

    def exist_xpath(self, path):
        """
        查看Xpath元素是否存在
        """
        node = self.find_elements_by_xpath(path)
        if node is None or len(node) == 0:
            return False
        else:
            return True

    def sleep(self, sleep_time=1):
        """
        睡眠x秒
        :param sleep_time:
        :return:
        """
        time.sleep(sleep_time)

    def double_click(self, node):
        """
        双击节点
        :param node:
        :return:
        """
        if node is str:
            node = self.find_element_by_xpath(node)
        ActionChains(self).double_click(node).perform()

    def context_click(self, node):
        """
        右键节点
        :param node:
        :return:
        """
        if node is str:
            node = self.find_element_by_xpath(node)
        ActionChains(self).context_click(node).perform()

    def drap_and_drop(self, target, toTarget):
        """
        拖拽效果
        :param target:
        :param toTarget:
        :return:
        """
        if target is str:
            target = self.find_element_by_xpath(target)
        if toTarget is str:
            toTarget = self.find_element_by_xpath(toTarget)
        ActionChains(self).drag_and_drop(target, toTarget)

    def switch_frame(self, xPath=None, node=None):
        """
        切入至frame
        :param xPath:
        :return:
        """
        assert xPath is not None or node is not None, "请输入定位标识"
        node = self.find_element_by_xpath(xPath) if xPath is not None else node
        self.switch_to.frame(node)

    def switch_parent_frame(self):
        """
        切换父类界面
        :return:
        """
        self.switch_to.parent_frame()

    def switch_windows(self, window_node):
        """
        切换窗口
        :param window_node:窗口句柄
        :return:当前窗口句柄
        """
        self.switch_to.window(window_node)
        return window_node

    def switch_new_windows(self):
        """
        切换至最新页面
        :return:最新的窗口句柄
        """
        self.switch_to.window(self.window_handles[-1])
        return self.window_handles[-1]

    def set_memory_windows(self, name, windows=None):
        """
        设置记忆窗口
        :param name:  记忆窗口名字
        :param windows:记忆的窗口
        :return:
        """
        self.memory_windows[name] = self.current_window_handle if windows is None else windows
        return True

    def pop_memory_windows(self, name):
        """
        查看并删除窗口
        :param name:窗口句柄名
        :return:节点窗口
        """
        return None if name not in self.memory_windows else self.memory_windows.pop(name)

    def get_memory_windows(self, name):
        """
        查看窗口句柄
        :param name:窗口句柄名
        :return:窗口句柄
        """
        return None if name not in self.memory_windows else self.memory_windows[name]

    def switch_memort_windows(self, name):
        """
        切换至记忆窗口
        :param name:窗口句柄名
        :return:窗口句柄
        """
        return self.switch_windows(self.get_memory_windows(name))

    def scroll(self, hight=0, width=0):
        """
        滚动条
        :param hight: 向下高度 +
        :param width: 向右高度 +
        :return:
        """
        self.execute_script("window.scrollBy(" + str(width) + "," + str(hight) + ")")

    def focus(self, node):
        """
        设置焦点
        :param node:
        :return:
        """
        self.execute_script("arguments[0].focus();", node)

    def set_memory_cookie(self, name):
        """
        记忆cookie
        :param name:
        :return:
        """
        self._memory_cookies[name] = self.get_cookies()

    def pop_memory_cookie(self, name):
        """
        记忆cookie
        :param name:
        :return:
        """
        if name in self._memory_cookies:
            return self._memory_cookies.pop(name)
        else:
            raise Exception("cookie不存在")

    def load_memory_cookie(self, name):
        """
        加载记忆cookie
        :param name:
        :return:
        """
        assert name in self._memory_cookies, "无" + name + "cookie"
        self.delete_all_cookies()
        for item in self._memory_cookies[name]:
            self.add_cookie(item)
