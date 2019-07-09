import os


class FileTools:

    def save_file(self, path, file_name, content):
        """
        保存文件
        :param path:
        :param file_name:
        :param content:
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(path)  # 若不存在则创建目录
        if not isinstance(content, bytes):
            content = content.encode(encoding='utf-8')  # 解码为字节码
        with open(path + file_name, "wb") as fp:
            fp.write(content)

    def read_file(self, path, file_name):
        """
        读取文件
        :param path:
        :param file_name:
        :return:
        """
        with open(path + file_name, "rb") as fp:
            content = fp.read()
            content = content.decode(encoding='utf-8').strip()  # 解码为字符码
        return content

    def read_file_line(self, path, file_name):
        """
        按行读取文件
        :param path:
        :param file_name:
        :return:
        """
        with open(path + file_name, "rb") as fp:
            contents = fp.readlines()

        for i in range(len(contents)):
            contents[i] = contents[i].decode(encoding='utf-8').strip()  # 解码为字符码
        return contents

    def auto_search(self, seach_path, level=None):
        """
        嗅探文件
        :param seach_path:  搜索路径
        :param level:       嗅探层级
        :return: [(路径1,名字1),(路径2,名字2)]
        """
        if level == 0:
            return []
        file_info = []
        cateList = os.listdir(seach_path)
        for mydir in cateList:
            if os.path.isfile(seach_path + mydir):
                file_info.append((seach_path, mydir))
            else:
                classPath = seach_path + mydir + '/'
                if level is not None:
                    level -= level
                temp = self.auto_search(classPath, level)
                file_info.extend(temp)

        return file_info

    def delete_file(self, path, file):
        """
        删除文件
        :param path:
        :param file:
        :return:
        """
        os.remove(path + file)

    def delete_dir(self, path):
        """
        删除文件夹下的文件
        :param path:
        :return:
        """
        lst = self.auto_search(path)
        cnts = 0
        for item in lst:
            os.remove(item[0] + item[1])
            cnts += 1
        return cnts

    def create_dir(self, path):
        """
        创建文件夹
        :param path:
        :return:
        """
        if not os.path.exists(path):
            # 若不存在则创建目录
            os.makedirs(path)

    def exist(self, path):
        """
        判断文件/文件夹是否存在
        :param path:
        :return:
        """
        if os.path.exists(path):
            return True
        else:
            return False


file_tools = FileTools()
