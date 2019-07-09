from src.code.core.driver import DriverHelper, webdriver
from src.code.core.logging import LogHelper
from src.code.core.capture import CaptureHelper
from src.code.core.proxy import ProxyHelper
from src.code.core.file import FileHelper
from src.code.core.http import HttpHelper
from src.code.core.database import *
from browsermobproxy import Server
from src.code.tools import *
from src.code.config import *


class Scheduler:
    """
    调度中心,负责进程的调度
    """

    def __init__(self):
        # 任务名
        self._job_name: str = None
        # 浏览器句柄
        self._driver: DriverHelper = None
        # 系统日志
        self._sys_logger: LogHelper = None
        # 代理日志
        self._proxy_logger: LogHelper = None
        # 用户日志
        self._user_logger: LogHelper = None
        # 截图线程
        self._captureHelper: CaptureHelper = None
        # 代理助手
        self._proxyHelper: ProxyHelper = None
        # sql线程池
        self._sqlHelpers: dict = {}
        # 文件非阻塞保存队列
        self._fileHelper: FileHelper = None
        # ajax请求
        self._HttpHelper: HttpHelper = None

        # 清空缓存文件夹
        # file_tools.create_dir(GF.getCachePath())
        # file_tools.delete_dir(GF.getCachePath())

    def start_DriverHelper(self, job_name, windows_size: tuple or int = None,
                           headless=False, options=None, image=True, mute=False,
                           proxy=False, proxy_port=None) -> DriverHelper:
        """
        创建并初始化浏览器窗口,一切任务的开始
        :param job_name:        任务名称,必填
        :param windows_size:    (窗口宽,窗口高)
        :param headless:        是否静默模式
        :param options:         chrom启动选项
        :param image:           是否显示图片
        :param mute:            是否静音
        :param proxy:           是否代理
        :param proxy_port:      代理端口                浏览器句柄driver
        """
        assert self._driver is None, "浏览器已开启"

        self._job_name = job_name
        # 启动option设置
        if options is None:
            options = webdriver.ChromeOptions()

        # 启动系统日志
        self.init_system_log()

        if proxy:
            # 开启代理类,编辑浏览器启动项
            options = self._start_ProxyHelper(options, proxy_port)

        # 实例化浏览器类
        self._driver = DriverHelper(job_name, options=options, windows_size=windows_size,
                                    headless=headless, mute=mute, image=image)
        # 开启实例化图片捕捉
        self._start_CaptureHelper()

        # 赋予xpath_tools浏览器句柄,方便开发
        xpath_tools.set_driver(self._driver)

        return self._driver

    def _start_ProxyHelper(self, options, proxy_port=None):
        """
        启动代理类,用于监听Http请求
        :param options: chrom浏览器启动选项
        :param proxy_port: 代理端口号
        """
        assert self._proxyHelper is None, "代理已开启"
        # 代理端口,若未指定,获取默认端口
        proxy_port = GF.getProxyPort() if proxy_port is None else proxy_port

        # 启动代理浏览器
        server = Server(GF.getProxyPath(), {'port': proxy_port})
        server.start({'log_path': GF.getCachePath()})
        proxy = server.create_proxy()

        # 开启har监听
        proxy.new_har(options={'captureContent': True, 'captureHeaders': True})
        options.add_argument('--proxy-server={0}'.format(proxy.proxy))

        # 启动代理日志
        self.init_proxy_log()
        # 启动代理助手
        self._proxyHelper = ProxyHelper(self, proxy)

        return options

    def _start_CaptureHelper(self):
        """
        启动屏幕捕捉类
        """
        # 启动屏幕捕捉
        self._captureHelper = CaptureHelper(self)

        return self._captureHelper

    def start_SqlHelper(self, database_type: str = "MARIADB", defulat_name: str = None) -> DataBaseHelper:
        """
        启动数据库连接池
        :type defulat_name: 数据库默认名字,不填为default_name
        """
        database_type = database_type.upper()

        if database_type == 'MARIADB':
            SqlHelper = MariadbHelper
        elif database_type == 'MYSQL':
            SqlHelper = MysqlHelper
        elif database_type == 'ORACLE':
            SqlHelper = OrcaleHelper
        else:
            raise Exception(database_type+"数据库不支持")

        if database_type not in self._sqlHelpers:
            self._sqlHelpers[database_type] = SqlHelper(defulat_name)
        return self._sqlHelpers[database_type]

    def start_HttpHelper(self):
        """
        初始化接口测试类
        :param implementation_type: 实现类
        """

        if self._HttpHelper is not None:
            return self._HttpHelper

        # 初始化接口测试类
        self._HttpHelper = HttpHelper(self)

        return self._HttpHelper

    def start_user_log(self):
        """
        开启日志
        """
        if self._user_logger is not None:
            return self._user_logger

        # 初始化类
        self._user_logger = LogHelper(self._job_name)
        # 设置控制台显示
        self._user_logger.add_ConsoleHandler()
        # 设置文件显示
        self._user_logger.add_FileHandler()

        return self._user_logger

    def get_job_name(self):
        """
        获取任务名
        """
        return self._job_name

    def get_HttpHelper(self):
        """
        获取Http助手
        """
        assert self._HttpHelper is not None, "未初始化接口"

        return self._HttpHelper

    def get_ProxyHelper(self):
        """
        获取代理助手
        """
        assert self._proxyHelper is not None, "未初始化代理助手"

        return self._proxyHelper

    def get_SqlHelpers(self, database_type="MARIADB") -> DataBaseHelper:
        """
        获取sql助手
        """
        database_type = database_type.upper()

        assert database_type in self._sqlHelpers, database_type + "数据助手未初始化"

        return self._sqlHelpers[database_type]

    def get_CaptureHelper(self):
        """
        获取捕捉助手
        """
        assert self._driver is not None, "浏览器未开启"
        assert self._captureHelper is not None, "未开启截屏助手"

        return self._captureHelper

    def get_DriverHelper(self):
        """
        获取浏览器句柄
        """
        assert self._driver is not None, "未开启浏览器"

        return self._driver

    def get_user_log(self):
        """
        获取用户日志
        """
        assert self._user_logger is not None, "未开启日志"

        return self._user_logger

    def find_system_logger(self):
        """
        获取系统日志
        """
        assert self._sys_logger is not None, "系统日志未初始化"

        return self._sys_logger

    def find_proxy_logger(self):
        """
        获取代理日志
        """
        assert self._proxy_logger is not None, "代理日志未初始化"

        return self._proxy_logger

    def find_system_fileHelper(self):
        """
        获取文件保存类
        """
        assert self._fileHelper is not None, "文件保存类未初始化"

        return self._fileHelper

    def init_system_fileHelper(self):
        """
        启动文件保存类
        """
        if self._fileHelper is not None:
            return self._fileHelper
        # 初始化系统日志
        self.init_system_log()

        # 启动文件线程
        self._fileHelper = FileHelper(self)
        # 开启文件异步保存线程
        self._fileHelper.runner_start()

        return self._fileHelper

    def init_system_log(self):
        """
        初始化系统日志
        """
        if self._sys_logger is not None:
            return self._sys_logger
        # 启动日志助手
        self._sys_logger = LogHelper(self._job_name, suffix='_system.txt')
        # 添加文件夹记录
        self._sys_logger.add_FileHandler()
        return self._sys_logger

    def init_proxy_log(self):
        """
        初始化代理监听日志
        """
        if self._proxy_logger is not None:
            return self._proxy_logger

        self._proxy_logger = LogHelper(self._job_name, suffix='_proxy.txt')
        # 添加代理记录
        self._proxy_logger.add_FileHandler()
        return self._proxy_logger

    def show_console(self, msg, level="D"):
        """
        自动选择控制台显示方式
        :param msg:
        :param level:
        :return:
        """
        if self._user_logger is not None:
            level = level.upper()
            if level == "D":
                self._user_logger.debug(msg)
            elif level == "I":
                self._user_logger.info(msg)
            elif level == "E":
                self._user_logger.error(msg)
            elif level == "W":
                self._user_logger.warning(msg)
            else:
                raise Exception("打印级别" + level + "错误")
        else:
            if level == "E":
                print("\033[0;31;m", msg, "\033[0m")
            else:
                print(msg)
