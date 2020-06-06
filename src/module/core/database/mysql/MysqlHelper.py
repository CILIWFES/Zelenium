from ..base.DataBaseHelper import DataBaseHelper
import time
import datetime


class MysqlHelper(DataBaseHelper):

    def __init__(self, defualt_name):

        super().__init__(defualt_name)

    def _connect(self, url, userName, password, database, connect_name, charset):
        import pymysql
        """
        建立数据库连接
        :param url:
        :param userName:
        :param password:
        :param database:
        :param connect_name:
        :return:
        """
        if charset is None:
            charset = 'utf8'
        connect = None
        times = 10
        now_time = 0
        wait_time = 2
        while now_time < times:
            try:
                connect = pymysql.connect(url, userName, password, database, charset=charset)
                break
            except:
                print("\033[0;31;m 数据库连接失败 \033[0m")
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
            return f"str_to_date('{data.strftime('%Y-%m-%d %H:%M:%S')}','%Y-%m-%d %H:%i:%S')"
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
            cursor.execute("""show variables like 'character_set_database'""")
            results = cursor.fetchone()
            result = self._splice_dict([results], cursor.description)
            return result[0]['character_set_database'] if len(result) == 1 else None
        except Exception as e:
            raise Exception(str(e))
