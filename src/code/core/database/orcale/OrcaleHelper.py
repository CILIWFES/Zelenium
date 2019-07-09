from ..base.DataBaseHelper import DataBaseHelper
import cx_Oracle as orcale
import os
import time
import datetime


class OrcaleHelper(DataBaseHelper):

    def __init__(self, defualt_name):

        super().__init__(defualt_name)

    def _connect(self, url, userName, password, sid, connect_name, charset):
        """
        建立数据库连接
        :param url:
        :param userName:
        :param password:
        :param sid:
        :param connect_name:
        :return:
        """
        # 设置编码
        if charset is None:
            charset = 'SIMPLIFIED CHINESE_CHINA.UTF8'

        connect = None
        times = 10
        now_time = 0
        wait_time = 2

        while now_time < times:
            try:
                os.environ['NLS_LANG'] = charset
                connect = orcale.connect(f"""{userName}/{password}@{url}/{sid}""")
                break
            except Exception as e:
                print(f"\033[0;31;m 数据库连接失败:{str(e)} \033[0m")
                time.sleep(wait_time)
            now_time += 1

        return connect

    def data_str(self, data):
        """
        数据转str格式,便于传输
        :param data:
        :return:
        """
        if isinstance(data, datetime.datetime):
            return f"to_date('{data.strftime('%Y-%m-%d %H:%M:%S')}','yyyy-mm-dd HH24:mi:ss')"
        else:
            return f"'{str(data)}'"

    def _get_charset(self, connect):
        """
        获取数据库编码
        :param connect:
        :return:
        """
        cursor = connect.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute("""select userenv('language') from dual""")
            result = cursor.fetchone()
            return result
        except Exception as e:
            raise Exception(str(e))

    def _get_connnect(self, database_name):
        """
        获取可用连接
        :param database_name:
        :return:
        """
        if database_name is None:
            database_name = self._default_name

        assert database_name in self._connections, database_name + "不在数据库池中"

        connect = self._connections[database_name]

        return connect
