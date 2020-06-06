import cv2
import base64
import math
import numpy as np


class ImageTools:

    def binarization(self, gray, threshold):
        """
        二值化
        :param gray:
        :return:
        """
        ret, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return binary

    def noise_remove(self, gray_img, k):
        """
        去噪点
        :param gray_img: 灰度图片
        :param k 阈值
        :return:
        """
        h, w = gray_img.shape
        for _w in range(w):
            for _h in range(h):

                # 计算邻域非白色的个数
                pixel = gray_img[_h, _w]
                if pixel == 255:
                    continue
                if self.__calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img[_h, _w] = 255
        return gray_img

    def __calculate_noise_count(self, img_obj, w, h):
        """
        计算邻域非白色的个数
        :param img_obj: img obj
        :param w: width
        :param h: height
        :return: count (int)
        """
        count = 0
        height, width = img_obj.shape
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj[_h_, _w_] != 255:  # 这里因为是灰度图像，设置小于230为非白色
                    count += 1
        return count

    def base64_to_gray(self, base64_code):
        """
        base64 转化numpy
        :param base64_code:
        :return:
        """
        data = base64.b64decode(base64_code)
        nparr = np.fromstring(data, np.uint8)
        img = cv2.imdecode(nparr, 0)
        return img

    def show_Grayscale(self, imgs: np.ndarray, labels: np.ndarray = None):
        """
        显示灰度图片
        :param imgs: [图片数, 高, 宽] or [高, 宽]
        :param labels:
        :return:
        """
        if len(imgs.shape) == 2:
            img_size = 1
            showImgs = [imgs]
        elif len(imgs.shape) == 3:
            img_size = imgs.shape[0]
            showImgs = imgs
        else:
            raise Exception("错误传入类型")

        if labels is not None and labels.shape[0] != img_size:
            raise Exception("输入图片与标签不符合")
        matrix_size = math.ceil(pow(img_size, 0.5))

        self._showPyplot(showImgs, img_size, matrix_size, labels=labels, cmap='Greys_r')

    def _showPyplot(self, showImgs, img_size, matrix_size, cmap=None, labels=None):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        # 向上转型
        for i in range(img_size):
            # 添加图层
            ax = fig.add_subplot(matrix_size, matrix_size, i + 1)
            # 设置标签
            if labels is not None:
                ax.set_title(labels[i])
            # 图像展示
            if cmap is None:
                plt.imshow(showImgs[i])
            else:
                plt.imshow(showImgs[i], cmap=cmap)

            # 坐标轴关闭
            plt.axis("off")
        # 图层展示
        plt.show()

    # cv2.INTER_NEAREST最近邻插值
    # cv2.INTER_LINEAR 线性插值
    # cv2.CV_INTER_AREA：区域插值
    # cv2.INTER_CUBIC 三次样条插值
    # cv2.INTER_LANCZOS4 Lanczos插值
    def resize(self, picture, toWidth=0, toHigh=0, mode=cv2.INTER_LINEAR, isChannelPicture=False):
        """
        缩放图片
        :param picture:
        :param toWidth:
        :param toHigh:
        :param mode:
        :param isChannelPicture:
        :return:
        """
        toWidth = math.ceil(toWidth)
        toHigh = math.ceil(toHigh)

        if isChannelPicture:
            changePicture = cv2.resize(picture, (toWidth, toHigh), mode)
        else:
            if isinstance(picture, list):
                changePicture = np.array([cv2.resize(item, (toWidth, toHigh), mode) for item in picture])
            else:
                changePicture = cv2.resize(picture, (toWidth, toHigh), mode)

        return changePicture


image_tools = ImageTools()
