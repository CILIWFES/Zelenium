class DataBaseHelper:
    def __init__(self, data_name=None):
        self._connections = {}
        self._default_name = data_name

    def connect(self, url, userName, password, database, connect_name=None, charset=None):
        """
        初始化连接
        :param url:
        :param userName:
        :param password:
        :param database:
        :param connect_name:
        :return:
        """
        if connect_name is None:
            connect_name = "defalut"

        connect = self._connect(url, userName, password, database, connect_name, charset)

        if self._default_name is None:
            self._default_name = connect_name

        if connect_name in self._connections:
            self._connections[connect_name].close()

        # 加入连接池
        self._connections[connect_name] = connect
        return connect

    def set_default_name(self, default_name):
        self._default_name = default_name

    def _connect(self, url, userName, password, database, connect_name, charse):
        pass

    def selectAll(self, sql, database_name=None, size=None) -> list:
        """
        查询多条
        :param size:
        :param sql:
        :param database_name:
        :return:
        """
        connect = self._get_connnect(database_name)
        cursor = connect.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql.upper())
            if size is not None:
                results = cursor.fetchmany(size)
            else:
                results = cursor.fetchall()
            return self._splice_dict(results, cursor.description)
        except Exception as e:
            raise Exception(str(e))

        return None

    def selectOne(self, sql, database_name=None) -> list:
        """
        查询单条
        :param sql:
        :param force:
        :param database_name:
        :return:
        """
        connect = self._get_connnect(database_name)

        cursor = connect.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql.upper())

            results = cursor.fetchone()
            result = self._splice_dict([results], cursor.description)
            return result[0] if len(result) == 1 else None

        except Exception as e:
            raise Exception(str(e))

        return None

    def update(self, sql=None, table=None, data=None, where=None, auto_commit=True,
               database_name=None) -> int:
        """
        更新数据
        :param sql:
        :param table:
        :param data:
        :param where:
        :param database_name:
        :param auto_commit:
        :return:
        """
        connect = self._get_connnect(database_name)
        if auto_commit:
            connect.begin()

        cursor = connect.cursor()
        sql = sql if sql is not None else f"""update {table} set {" , ".join(self.dict_list(data))} where {where}"""

        try:
            cursor.execute(sql)

            if auto_commit:
                connect.commit()

            return cursor.rowcount
        except Exception as e:
            if auto_commit:
                connect.rollback()
            raise Exception(str(e))

    def insert(self, sql=None, table=None, data=None, auto_commit=True, database_name=None) -> int:
        """
        插入数据
        :param sql:
        :param table:
        :param data:
        :param database_name:
        :param auto_commit:
        :return:
        """
        connect = self._get_connnect(database_name)
        if auto_commit:
            connect.begin()

        cursor = connect.cursor()
        if sql is None:
            condition = []
            condition_data = []
            for key, item in data.items():
                condition.append(key)
                condition_data.append(item)
            sql = f"""insert into {table} ({" , ".join([f"{key}" for key in condition])}) VALUE({" , ".join(
                [f"{self.data_str(data)}" for data in condition_data])})"""

        try:
            cursor.execute(sql)

            if auto_commit:
                connect.commit()
            return cursor.rowcount

        except Exception as e:
            if auto_commit:
                connect.rollback()
            print(str(e))
            raise Exception(e)

    def delete(self, sql=None, table=None, where=None, auto_commit=True, database_name=None) -> int:
        """
        删除数据
        :param sql:
        :param table:
        :param where:
        :param database_name:
        :param auto_commit:
        :return:
        """
        connect = self._get_connnect(database_name)
        if auto_commit:
            connect.begin()

        cursor = connect.cursor()
        if sql is None:
            sql = f"""delete from {table} where {where} """

        try:
            cursor.execute(sql)
            if auto_commit:
                connect.commit()

            return cursor.rowcount

        except Exception as e:
            if auto_commit:
                connect.rollback()
            raise Exception(str(e))

    def commit(self, database_name=None):
        """
        手动提交
        :param database_name:
        :return:
        """
        connect = self._get_connnect(database_name)
        connect.commit()

    def rollback(self, database_name=None):
        """
        手动回滚
        :param database_name:
        :return:
        """
        connect = self._get_connnect(database_name)
        connect.rollback()

    def _splice_dict(self, results, description):
        """
        把查询结果拼接为字典
        :param results:
        :param description:
        :return:
        """
        retuen_dict = [{description[index][0]: item[index] for index in range(len(item))} for item in results]
        return retuen_dict

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

    def _get_charset(self, connect):
        """
        获取数据库编码
        :param connect:
        :return:
        """
        pass

    def data_str(self, data):
        """
        数据转str格式,便于传输
        :param data:
        :return:
        """
        pass

    def dict_list(self, data: dict):
        """
        字典转list
        :param data:
        :return:
        """
        return [f"{key}= {self.data_str(item)}" for key, item in data.items()]

    def __del__(self):
        for key, item in self._connections.items():
            item.close()
        del self
