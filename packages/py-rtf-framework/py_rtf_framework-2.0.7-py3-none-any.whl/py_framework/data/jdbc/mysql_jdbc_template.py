from typing import Any
import pandas as pd
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate, DbConfig
from py_framework.data.jdbc.sql_formatter import format_sql


class MysqlJdbcTemplate(BaseJdbcTemplate):
    """mysql的jdbc模板类"""

    def __init__(self, db_config: DbConfig):
        super().__init__(db_config)

    def _get_client(self):
        conn = pymysql.connect(host=self.db_config.host, port=self.db_config.port,
                               user=self.db_config.user, passwd=self.db_config.password,
                               db=self.db_config.database)
        # 获取一个游标对象
        cursor = conn.cursor()
        return conn, cursor

    def query(self, sql: str, param: dict[str, Any] = None) -> list[dict[str, Any]]:
        conn, cursor = self._get_client()
        cursor.execute(format_sql(sql, param))
        values = cursor.fetchall()
        self._close(conn, cursor)
        return values

    def query_for_df(self, sql: str, param: dict[str, Any] = None) -> pd.DataFrame:
        conn, cursor = self._get_client()
        cursor.execute(format_sql(sql, param))
        values = cursor.fetchall()
        # 获取列
        columns = []
        for item in cursor.description:
            columns.append(item[0])
        self._close(conn, cursor)
        return pd.DataFrame(data=values, columns=columns)

    def insert_df(self, table_name: str, record_df: pd.DataFrame):
        conn, cursor = self._get_client()
        insert_sql = f'insert into {table_name}(' + ','.join(record_df.columns) + ') values(' + \
                     ','.join(['%s'] * len(record_df.columns)) + ')'
        cursor.executemany(insert_sql, record_df.values.tolist())
        self._close(conn, cursor)

    def execute(self, sql: str, param: dict[str, Any] = None):
        conn, cursor = self._get_client()
        cursor.execute(sql, param)
        self._close(conn, cursor)

    def _close(self, conn, cursor):
        # 提交
        conn.commit()
        # 关闭
        conn.close()
        cursor.close()
