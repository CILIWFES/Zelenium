import os
import sys


class GlobalConstant:
    # ----------------------------系统配置------------------------
    # 系统默认编码
    DFAULT_CHARSET = sys.getdefaultencoding()

    # 工程路径
    SYS_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))) + "/"
    # 文件夹路径
    SYS_FILES_PATH = SYS_ROOT_PATH + "resource/"
    # 配置文件路径
    SYS_CONFIG_FOLDER = "config/"
    # 配置文件名
    SYS_GLO_CONFIG_FILENAME = "config.ini"
    # 配置文件路径
    SYS_GLO_CONFIG_PATH = SYS_FILES_PATH + SYS_CONFIG_FOLDER + SYS_GLO_CONFIG_FILENAME

    # 应用路径
    SYS_APPLICATION_PATH = "SYS_APPLICATION_PATH"
    # 通用分隔符
    SEPARATOR = '_'

    # 使用内嵌谷歌
    EMBEDDED_CHROM = "EMBEDDED_CHROM"

    # 谷歌路径
    SYS_CHROM_PATH = "SYS_CHROM_PATH"

    # 谷歌默认路径
    SYS_CHROM_DEFAULT_PATH = "SYS_CHROM_DEFAULT_PATH"

    # 缓存路径
    CACHE_PATH = "CACHE_PATH"

    # 模板路径
    TEMPLATE_PATH = "TEMPLATE_PATH"

    # excel模板路径
    TEMPLATE_EXCEL_PATH = "TEMPLATE_EXCEL_PATH"

    # 系统代理文件路径
    SYS_PROXY_PATH = "SYS_PROXY_PATH"

    # 无头模式下的屏幕尺寸
    HEADLESS_WINDOWS_SIZE = 'HEADLESS_WINDOWS_SIZE'

    # 全局Section
    G_SECTION = "ALL"

    # ---------------------------报告生成--------------------------

    # 生成测试报告时打印信息
    SHOW_PRINT_IN_CONSOLE = "SHOW_PRINT_IN_CONSOLE"
    # 显示报错信息
    SHOW_ERROR_TRACEBACK = "SHOW_ERROR_TRACEBACK"

    # 报告执行间隔
    REPORT_EXECUTE_INTERVAL = "REPORT_EXECUTE_INTERVAL"

    # 测试报告选择
    CREATE_REPORT_STYLE = "CREATE_REPORT_STYLE"
    # ---------------------------------工作文件分类---------------------------

    # 结果集路径
    SYS_RESULT_FOLDER = SYS_FILES_PATH + "result/"

    HTML_PATH = "HTML_PATH"

    PICTURE_PATH = "PICTURE_PATH"

    VIEDO_PATH = "VIEDO_PATH"

    GIF_PATH = "GIF_PATH"

    LOGGING_PATH = "LOGGING_PATH"

    HTTP_PATH = "HTTP_PATH"

    # ---------------------------------代理分类分类---------------------------

    # 系统代理端口
    SYS_PROXY_PORT = "SYS_PROXY_PORT"

    # 代理频率
    PROXY_CYCLE = "PROXY_CYCLE"

    # ---------------------------截屏设置--------------------------
    # 截图频率
    SCREENSHOT_CYCLE = "SCREENSHOT_CYCLE"

    # ---------------------------视频 gif生成设置--------------------------
    # 默认FPS
    AUTO_FPS = 'AUTO_FPS'

    # 自动设置尺寸
    AUTO_SIZE = 'AUTO_SIZE'

    # ---------------------------非阻塞队列设置---------------------------
    # 文件线程保存频率
    FILERUNNER_CYCLE = "FILERUNNER_CYCLE"

    # 文件线程数量
    FILERUNNER_COUNT = "FILERUNNER_COUNT"

    # 文件队列最大长度
    FILE_QUEUE_SIZE = "FILE_QUEUE_SIZE"

    # -------------------------神经网络配置--------------------
    # 验证码识别module路径
    DISCERN_PATH = "DISCERN_PATH"
    # 神经网络基础路径
    ANN_PATH = "ANN_PATH"


GT = GlobalConstant()
