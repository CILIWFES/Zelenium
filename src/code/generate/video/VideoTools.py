from src.code.config import *
from src.code.tools import *
import PIL.Image as Image
import os
import cv2


class VideoTools:

    def create_gif(self, job_name, time=None, fps=None, size=None):
        """
        创建gif
        :param job_name:
        :param time:
        :param fps:
        :param size:
        :return:
        """

        path = GF.gif_path(job_name)
        file_tools.create_dir(path)
        file_tools.delete_dir(path)

        search_path = GF.picture_path(job_name)
        pictures = file_tools.auto_search(search_path)

        if size is None:
            size = Image.open(pictures[0][0] + pictures[0][1]).size
            size = (size[0], size[1])

        self.__sort_picture(pictures)

        if time is not None:
            fps = len(pictures) // time

        fps = GF.auto_fps() if fps is None else fps

        self.__show_info(fps, size, len(pictures))

        frames = []
        for picture in pictures:
            img = Image.open(picture[0] + picture[1])
            if img.size[0] != size[0] or img.size[1] != size[1]:
                img = cv2.resize(img, (size[0], size[1]), cv2.INTER_LINEAR)
            frames.append(img)
        frames[0].save(path + job_name + '.gif', save_all=True, append_images=frames, duration=1 / fps)

        cmd = path
        cmd = cmd.replace('/', '\\')
        os.system('explorer.exe /e,' + cmd)
        print("生成GIF完成")

    def create_video(self, job_name, time=None, fps=None, size=None):
        """
        创建视频
        :param job_name:
        :param time:
        :param fps:
        :param size:
        :return:
        """

        path = GF.viedo_path(job_name)
        file_tools.create_dir(path)
        file_tools.delete_dir(path)

        search_path = GF.picture_path(job_name)
        pictures = file_tools.auto_search(search_path)
        self.__sort_picture(pictures)
        if size is None:
            size = cv2.imread(pictures[0][0] + pictures[0][1]).shape[:-1]
            size = (size[1], size[0])

        if time is not None:
            fps = len(pictures) // time

        fps = GF.auto_fps() if fps is None else fps

        self.__show_info(fps, size, len(pictures))

        # 指定写视频的格式, I420-avi, MJPG-mp4
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # 视频保存在当前目录下
        video = cv2.VideoWriter(path + job_name + '.avi', fourcc, fps, size)

        for item in pictures:
            img = cv2.imread(item[0] + item[1])

            if img.shape[1] != size[0] or img.shape[0] != size[1]:
                img = cv2.resize(img, (size[0], size[1]), cv2.INTER_LINEAR)
            video.write(img)

        video.release()
        cmd = path
        cmd = cmd.replace('/', '\\')
        os.system('explorer.exe /e,' + cmd)
        print("生成视频完成")

    def __show_info(self, fps, size, counts):
        print("帧率:", fps)
        print("图片尺寸(宽,高):", size)
        print("图片数量:", counts)
        print("预计时长:", counts / fps)

    def __sort_picture(self, picturs: list):

        picturs.sort(key=lambda x: int(x[1][x[1].find('_') + 1:x[1].find('.')]))


video_tools = VideoTools()
