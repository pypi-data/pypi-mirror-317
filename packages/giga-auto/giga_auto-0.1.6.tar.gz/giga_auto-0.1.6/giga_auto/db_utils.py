import pymysql

from giga_auto.logger import db_log


class DBUtils():

    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    def mysql_connect(self):
        self.conn = pymysql.connect(
            host=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            database=self.db_config["db_name"],
            charset=self.db_config["db_charset"]
        )
        return self.conn

    @db_log
    def db_execute(self, sql, args=None):
        cursor = self.conn.cursor()
        if args:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql)
        self.conn.commit()
        return cursor

    @db_log
    def db_fetchone(self, sql, args=None, dict_cursor=None):
        cursor = self.conn.cursor()
        if dict_cursor:
            cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        if args:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql)
        return cursor.fetchone()

    @db_log
    def db_fetchall(self, sql, args=None, dict_cursor=None):
        cursor = self.conn.cursor()
        if dict_cursor:
            cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        if args:
            cursor.executemany(sql, args)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
