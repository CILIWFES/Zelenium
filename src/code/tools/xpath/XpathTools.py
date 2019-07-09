from collections import Iterable


class XpathTools:

    def __init__(self):
        self._driver = None

    def set_driver(self, driver):
        self._driver = driver

    def find_internal_nodes(self, search_xpath, nodes=None, nodes_xpath=None):
        """
        逐数组,解析xpath过滤并获取对应节点
        :param nodes:
        :param search_xpath:
        :return: 找到的元素list
        """
        nodes = self.__adaptation(nodes, nodes_xpath)

        lst = []
        for node in nodes:
            item = node.find_elements_by_xpath(search_xpath)
            if item is not None and len(item) >= 1:
                lst.extend(item)
        return lst

    def find_contain_xpth(self, search_xpath, nodes=None, nodes_xpath=None):
        """
        搜索数组中哪些元素包含xpath
        :param search_xpath:    查询的xpath
        :param nodes:     查询的节点 优先级高
        :param nodes_xpath:查询节点的xpath 优先级低
        :return: 包含节点
        """

        nodes = self.__adaptation(nodes, nodes_xpath)

        lst = []
        for node in nodes:
            item = node.find_elements_by_xpath(search_xpath)
            if item is not None and len(item) > 0:
                lst.append(node)
        return lst

    def find_contain_string(self, string, nodes_xpath=None, nodes=None, like=True):
        """
        搜索数组中哪些元素包含字符串
        :param xpath:
        :param like: 全部匹配
        :param nodes_xpath:
        :return: 包含节点
        """
        nodes = self.__adaptation(nodes, nodes_xpath)

        lst = []

        for node in nodes:
            item = node.get_attribute('textContent')
            if like:
                if item.find(string) >= 0:
                    lst.append(node)
            else:
                if item == string:
                    lst.append(node)
        return lst

    def __adaptation(self, nodes=None, nodes_xpath=None):
        """
        通过输入的参数获取nodes
        :param nodes:
        :param nodes_xpath:
        :return:
        """
        assert nodes is not None or nodes_xpath is not None, "请输入节点或节点Xpath"

        nodes = self._driver.get_nodes_available(nodes_xpath) if nodes is None else nodes

        if not isinstance(nodes, Iterable):
            nodes = [nodes]
        return nodes


xpath_tools = XpathTools()
