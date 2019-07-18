import pytesseract


class OCRDiscern:
    def cleanImage(self, image):
        # 灰度
        image = image.convert('L')
        image = image.point(lambda x: 0 if x < 130 else 255)  # 对像素点处理
        image = self.noise_remove_pil(image, 3)
        return image

    def discern(self, image, lang=None):
        text = pytesseract.image_to_string(image, lang=lang)
        replace = text.replace(" ", "").replace("\n", "")
        return replace

    def noise_remove_pil(self, gray_img, k):
        """
        :param image_name: 图片文件命名
        :param k: 判断阈值
        :return:
        """
        w, h = gray_img.size
        for _w in range(w):
            for _h in range(h):

                # 计算邻域非白色的个数
                pixel = gray_img.getpixel((_w, _h))
                if pixel == 255:
                    continue
                if self.__calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img.putpixel((_w, _h), 255)
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
        width, height = img_obj.size
        for _w_ in [w - 1, w, w + 1]:
            for _h_ in [h - 1, h, h + 1]:
                if _w_ > width - 1:
                    continue
                if _h_ > height - 1:
                    continue
                if _w_ == w and _h_ == h:
                    continue
                if img_obj.getpixel((_w_, _h_)) != 255:  # 这里因为是灰度图像，设置小于230为非白色
                    count += 1
        return count


ocr_tools = OCRDiscern()
