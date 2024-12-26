# -*- coding: utf-8 -*-
from pymysql.cursors import DictCursor


class mysql_tools(object):
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        """
        启动连接
        :return:
        """
        cursor = self.conn.cursor(cursor=DictCursor)
        return cursor

    def connect_close(self):
        """
        关闭连接
        :return:
        """
        self.conn.close()

    @staticmethod
    def is_args(args_):
        if args_:
            if args_[0]:
                return args_
            else:
                return ''
        else:
            return ''

    def fetch_all(self, sql, *args):
        """
        批量查询
        :param sql:
        :param args:([])
        :return:
        """
        args = self.is_args(args)
        cursor = self.connect()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            record_list = cursor.fetchall()
        finally:
            cursor.close()
        return record_list

    def fetch_one(self, sql, *args):
        """
        查询单条数据
        :param sql:
        :param args:([])
        :return:
        """
        args = self.is_args(args)
        cursor = self.connect()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            result = cursor.fetchone()
        finally:
            cursor.close()

        return result

    def execute_sql(self, sql, *args):
        """
        :param sql:
        :param args:([])
        :return:
        """
        args = self.is_args(args)
        cursor = self.connect()
        try:
            if args:
                row = cursor.execute(sql, args)
            else:
                row = cursor.execute(sql)
            self.conn.commit()
        finally:
            cursor.close()
        return row

    def database_name(self):
        """
        获取数据库名
        """
        db_name = self.conn.db.decode('utf-8')
        return db_name
