from src.code.core import *
from .Page import *


class Table:
    def __init__(self, driver: DH, id_xpath):
        self.driver = driver
        self.id_xpath = id_xpath
        self.cols: list = {}
        self.current_page = Page()
        # 查询按钮
        self.search_node = None
        self.initialization()
        self.cols_dict: dict = {key: indx for indx, key in enumerate(self.cols)}

    def initialization(self):
        pass

    def reload(self, isSearch=True, search_node=None):
        """
        重新加载表格
        :param isSearch:    通过查询按钮重载
        :param search_node: 查询按钮句柄
        :return:
        """
        pass

    def next_page(self):
        """
        进入下一页
        :return:
        """
        pass

    def befor_page(self):
        """
        进入上一页
        :return:
        """
        pass

    def jump_page(self, num):
        """
        跳入指定页
        :return:
        """
        pass

    def get_info(self):
        """
        获取节点信息
        :return: [当前页数,总页数,一页几行,当前行数]
        """
        pass

    def get_row_node(self, indexs: int or list):
        """
        获取行节点
        :param indexs:
        :return:
        """
        if isinstance(indexs, int):
            indexs = [indexs]
        ret_lst = []

        for i in indexs:
            ret_lst.append(self.current_page.rows_node[i])
        return ret_lst if len(ret_lst) > 1 else ret_lst[-1]

    def get_clos(self, indexs: int or list, *args):
        """
        获取表格数据
        输入如:get_clos([0,2,4],"名字","性别")
        返回[ ['张三1','男'],['张三3','女'],['张三5','男']  ]
        :param indexs: 行号
        :param args:   字典值
        :return:
        """
        if isinstance(indexs, int):
            indexs = [indexs]
        key_indexs = [self.cols_dict[key] for key in args]
        ret_lst = []
        for i in indexs:
            lst = [self.current_page.rows[i][j] for j in key_indexs]
            ret_lst.append(lst)
        return ret_lst

    # 重载操作符
    def __getitem__(self, index: slice or tuple) -> list:
        rg1, rg2 = None, None
        if isinstance(index, slice):
            rg1 = self.__makeSlice__(index, len(self.current_page.rows))
            rg2 = slice(0, len(self.cols), 1)
        elif isinstance(index, tuple):
            rg1 = self.__makeSlice__(index[0], len(self.current_page.rows))
            rg2 = self.__makeSlice__(index[1], len(self.cols))
        retLst = []
        for rowIdx in range(rg1.start, rg1.stop, rg1.step):
            lst = []
            for colIdx in range(rg2.start, rg2.stop, rg2.step):
                lst.append(self.current_page.rows[rowIdx][colIdx])
            retLst.append(lst)
        return retLst

    # 切片编辑
    def __makeSlice__(self, index: slice, length):
        start = index.start if index.start is not None else 0
        stop = index.stop if index.stop is not None else length
        step = index.step if index.step is not None else 1
        assert start >= 0, "输入初始坐标错误"
        assert stop >= 0, "输出初始坐标错误"
        assert stop <= length, "长度超出限制,输入:" + str(stop) + "目标:" + str(length)
        assert step > 0, "步长错误"
        assert start <= stop, "区间错误"
        return slice(start, stop, step)
