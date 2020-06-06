import configparser
from .Constant import GT


class Configuration:

    def __init__(self):
        self.__GConfig = configparser.ConfigParser()
        self.__GConfig.read(GT.SYS_GLO_CONFIG_PATH, encoding='utf-8')

    def get_config(self, name, section=GT.G_SECTION):
        return self.__GConfig.get(section, name)

    def get_fils_path(self, names, section=GT.G_SECTION):
        """
        根据传入类型,拼接文件路径
        :param names:
        :param section:
        :return:
        """
        path = GT.SYS_FILES_PATH
        if type(names) is str:
            path += self.get_config(names, section)
            return path
        for item in names:
            path += self.get_config(item, section)
        return path

    def chrom_path(self):
        """
        获取谷歌浏览器路径
        :return:
        """
        if self.get_config(GT.EMBEDDED_CHROM) == 'True':
            return self.get_fils_path([GT.SYS_APPLICATION_PATH, GT.SYS_CHROM_DEFAULT_PATH])
        else:
            return self.get_config(GT.SYS_CHROM_PATH)

    def proxy_path(self):
        """
        获取代理应用路径
        :return:
        """
        return self.get_fils_path([GT.SYS_APPLICATION_PATH, GT.SYS_PROXY_PATH])

    def proxy_port(self):
        """
        获取代理端口号
        :return:
        """
        return int(self.get_config(GT.SYS_PROXY_PORT))

    def html_path(self, job_name):
        """
        拼接html保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.HTML_PATH, GT.G_SECTION)

    def log_path(self, job_name):
        """
        拼接日志保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.LOGGING_PATH, GT.G_SECTION)

    def http_path(self, job_name):
        """
        拼接接口代码保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.HTTP_PATH, GT.G_SECTION)

    def picture_path(self, job_name):
        """
        拼接图片保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.PICTURE_PATH, GT.G_SECTION)

    def viedo_path(self, job_name):
        """
        拼接视频保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.VIEDO_PATH, GT.G_SECTION)

    def gif_path(self, job_name):
        """
        拼接gif保存文件夹
        :param job_name:  工作名称
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_config(GT.GIF_PATH, GT.G_SECTION)

    def excel_path(self):
        """
        获取excel模板基础路径
        :return:
        """
        return self.get_fils_path([GT.TEMPLATE_PATH, GT.TEMPLATE_EXCEL_PATH], GT.G_SECTION)

    def cache_path(self):
        """
        获取缓存路径
        :return:
        """
        return self.get_fils_path([GT.CACHE_PATH], GT.G_SECTION)

    def file_path(self, job_name):
        """
        获取默认保存路径
        :return:
        """
        return GT.SYS_RESULT_FOLDER + job_name + "/" + self.get_fils_path([GT.DEFAULT_FILE_PATH], GT.G_SECTION)

    def auto_fps(self):
        """
        默认帧率
        :return:
        """
        return int(self.get_config(GT.AUTO_FPS, GT.G_SECTION))

    def auto_size(self):
        """
        生成视频或gif的默认尺寸(宽,高,是否开启)
        :return:
        """
        tup = eval(self.get_config(GT.AUTO_SIZE, GT.G_SECTION))
        if tup[-1]:
            return tup[:-1]
        else:
            return None

    def headless_windows_size(self):
        """
        无头模式下的浏览器尺寸
        :return:
        """
        import tkinter
        return tkinter.Tk().maxsize()

    def show_print_in_console(self):
        """
        生成测试报告时打印信息
        :return:
        """
        return self.get_config(GT.SHOW_PRINT_IN_CONSOLE) == 'True'

    def show_error_traceback(self):
        """
        显示报错信息
        :return:
        """
        return self.get_config(GT.SHOW_ERROR_TRACEBACK) == 'True'

    def report_execute_interval(self):
        """
        显示报错信息
        :return:
        """
        return float(self.get_config(GT.REPORT_EXECUTE_INTERVAL))

    def ann_discern_path(self, name):
        """
        获取验证码识别文件夹
        :param name:
        :return:
        """
        return self.get_fils_path([GT.ANN_PATH, GT.DISCERN_PATH]) + name + "/"

    def create_report(self, style_no):
        """
        判断是否创建测试报告
        :param style_no: 报告序号
        :return:
        """
        style_no = int(style_no)
        lst = eval(self.get_config(GT.CREATE_REPORT_STYLE))
        if style_no in lst:
            return True
        else:
            return False

    def zoom_rate(self):
        """
        获取Windows的缩放比例,用于截图
        :return:
        """
        return float(self.get_config(GT.ZOOM_RATE))
