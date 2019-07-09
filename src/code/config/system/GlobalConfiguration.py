import configparser
from .GlobalConstant import GT


class GlobalConfiguration:

    def __init__(self):
        self.__GConfig = configparser.ConfigParser()
        self.__GConfig.read(GT.SYS_GLO_CONFIG_PATH, encoding='utf-8')

    def getConfig(self, name, section=GT.G_SECTION):
        return self.__GConfig.get(section, name)

    def getFilsPath(self, names, section=GT.G_SECTION):
        """
        根据传入类型,拼接文件路径
        :param names:
        :param section:
        :return:
        """
        path = GT.SYS_FILES_PATH
        if type(names) is str:
            path += self.getConfig(names, section)
            return path
        for item in names:
            path += self.getConfig(item, section)
        return path

    def getChromPath(self):
        """
        获取谷歌浏览器路径
        :return:
        """
        if self.getConfig(GT.EMBEDDED_CHROM) == 'True':
            return self.getFilsPath([GT.SYS_APPLICATION_PATH, GT.SYS_CHROM_DEFAULT_PATH])
        else:
            return self.getConfig(GT.SYS_CHROM_PATH)

    def getProxyPath(self):
        """
        获取代理应用路径
        :return:
        """
        return self.getFilsPath([GT.SYS_APPLICATION_PATH, GT.SYS_PROXY_PATH])

    def getProxyPort(self):
        """
        获取代理端口号
        :return:
        """
        return int(self.getConfig(GT.SYS_PROXY_PORT))

    def getHtmlPath(self, job_name):
        """
        拼接html保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.HTML_PATH, GT.G_SECTION)

    def getLogPath(self, job_name):
        """
        拼接日志保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.LOGGING_PATH, GT.G_SECTION)

    def getHttpPath(self, job_name):
        """
        拼接接口代码保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.HTTP_PATH, GT.G_SECTION)

    def getPicturePath(self, job_name):
        """
        拼接图片保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.PICTURE_PATH, GT.G_SECTION)

    def getViedoPath(self, job_name):
        """
        拼接视频保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.VIEDO_PATH, GT.G_SECTION)

    def getGifPath(self, job_name):
        """
        拼接gif保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.getConfig(GT.GIF_PATH, GT.G_SECTION)

    def getExcelPath(self):
        """
        获取excel模板基础路径
        :return:
        """
        return self.getFilsPath([GT.TEMPLATE_PATH, GT.TEMPLATE_EXCEL_PATH], GT.G_SECTION)

    def getCachePath(self):
        """
        获取缓存路径
        :return:
        """
        return self.getFilsPath([GT.CACHE_PATH], GT.G_SECTION)

    def auto_fps(self):
        """
        默认帧率
        :return:
        """
        return int(self.getConfig(GT.AUTO_FPS, GT.G_SECTION))

    def auto_size(self):
        """
        生成视频或gif的默认尺寸(宽,高,是否开启)
        :return:
        """
        tup = eval(self.getConfig(GT.AUTO_SIZE, GT.G_SECTION))
        if tup[-1]:
            return tup[:-1]
        else:
            return None

    def headless_windows_size(self):
        """
        无头模式下的浏览器尺寸
        :return:
        """
        tup = eval(self.getConfig(GT.HEADLESS_WINDOWS_SIZE, GT.G_SECTION))
        return tup

    def show_print_in_console(self):
        """
        生成测试报告时打印信息
        :return:
        """
        return self.getConfig(GT.SHOW_PRINT_IN_CONSOLE) == 'True'

    def show_error_traceback(self):
        """
        显示报错信息
        :return:
        """
        return self.getConfig(GT.SHOW_ERROR_TRACEBACK) == 'True'

    def report_execute_interval(self):
        """
        显示报错信息
        :return:
        """
        return float(self.getConfig(GT.REPORT_EXECUTE_INTERVAL))

    def create_report(self, style_no):
        """
        判断是否创建测试报告
        :param style_no: 报告序号
        :return:
        """
        style_no = int(style_no)
        lst = eval(self.getConfig(GT.CREATE_REPORT_STYLE))
        if style_no in lst:
            return True
        else:
            return False
