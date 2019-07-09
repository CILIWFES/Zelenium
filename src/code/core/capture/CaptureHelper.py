from src.code.config import *
from .CaptureRunner import CaptureRunner
from PIL import Image
from io import BytesIO
from src.code.tools import *
import time


class CaptureHelper:
    def __init__(self, scheduler):
        """
        屏幕图像处理与线程支持
        :param scheduler: 调度中心
        """
        self._scheduler = scheduler
        self._captureRunner: CaptureRunner = None
        self._driver = self._scheduler.get_DriverHelper()
        self._job_name = self._scheduler.get_job_name()

    def screen_capture(self):
        """
        截屏,返回图片
        :return:
        """
        image = self._driver.get_screenshot_as_png()
        image = Image.open(BytesIO(image))
        return image

    def show_portion_image(self, node):
        """
        展示图片位置
        :param node:
        :return:
        """
        image = self.get_portion_image(node)
        image.show(GF.getCachePath() + str(int(time.clock())))
        return True

    def get_portion_image(self, node):
        """
        截取元素图片
        :param node: 截图节点
        :return:
        """
        js_ret = self._driver.execute_script('''
            var bounding_top = arguments[0].getBoundingClientRect();
            if(document.documentElement.scrollHeight > document.documentElement.clientHeight){
                arguments[0].scrollIntoView();  
                var rect_obj = arguments[0].getBoundingClientRect();
                if(rect_obj.top == 0){
                    return 'scroll-and-on-the-top';
                }else{
                    var size_array = new Array(4);
                    size_array[0] = rect_obj.x;
                    size_array[1] = rect_obj.y;
                    size_array[2] = rect_obj.right;
                    size_array[3] = rect_obj.bottom;
                    return size_array;
                }
            }else{
                return 'no-scroll';
            }
        ''', node)
        self._driver.execute_script('arguments[0].scrollIntoView();', node)
        image = self.screen_capture()
        _x, _y = node.location['x'], node.location['y']
        _h, _w = node.size['height'], node.size['width']
        if js_ret == 'scroll-and-on-the-top':
            size = (_x, 0, _x + _w, _h)
        elif js_ret == 'no-scroll':
            size = (_x, _y, _x + _w, _y + _h)
        else:
            size = tuple(js_ret)
        cropped = image.crop(size)

        return cropped

    def screenshot_byte(self):
        """
        截屏线程调用
        :return:
        """
        return self._driver.get_screenshot_as_png()

    def __init_file(self):
        """
        初始化文件夹
        :return:
        """
        file_tools.create_dir(GF.getPicturePath(self._job_name))
        file_tools.delete_dir(GF.getPicturePath(self._job_name))

    def runner_start(self, cycle=None):
        """
        启动线程
        :param force_start: 忽略配置直接开启截图
        :param cycle:       截图周期
        :return:
        """
        assert not self.runner_alive(), "线程已启动"

        # 初始化文件
        self._scheduler.init_system_fileHelper()

        if cycle is None:
            cycle = float(GF.getConfig(GT.SCREENSHOT_CYCLE))

        self._captureRunner = CaptureRunner(self._scheduler, cycle)

        self.__init_file()

        self._captureRunner.start()

    def runner_alive(self):
        """
        判断线程存活
        :return:
        """
        if self._captureRunner is None:
            return False

        return self._captureRunner.isAlive()

    def runner_wait(self, wait):
        """
        判断线程暂停
        :param wait:
        :return:
        """
        if self._captureRunner is None:
            return False
        self._captureRunner.wait(wait)

    def runner_stop(self, wait=True):
        """
        是否等待,默认阻塞等待线程终止
        :param wait:
        :return:
        """
        if self._captureRunner is None:
            return True
        self._captureRunner.stop(wait)

    def runner_cycle(self, new_cycle):
        """
        切换线程睡眠周期
        :param wait:
        :return:
        """
        if self._captureRunner is None:
            return False
        self._captureRunner.switch_cycle(new_cycle)
