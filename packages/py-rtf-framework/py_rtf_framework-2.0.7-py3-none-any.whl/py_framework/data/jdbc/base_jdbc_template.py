from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field
import pandas as pd
from enum import Enum


class DbType(str, Enum):
    """数据库类型"""

    MySql = "mysql"
    ClickHouse = "clickhouse"


class DbConfig(BaseModel):
    type: DbType = Field(title="数据库类型", default=DbType.MySql)
    host: str = Field(title="数据库IP地址", default=None)
    port: int = Field(title="数据库端口", default=None)
    user: str = Field(title="数据库连接账号", default=None)
    password: str = Field(title="数据库连接密码", default=None)
    database: str = Field(title="数据库", default=None)


class BaseJdbcTemplate(ABC):
    """基础jdbc模板类"""

    db_config: DbConfig

    def __init__(self, db_config: DbConfig):
        self.db_config = db_config

    @abstractmethod
    def query(self, sql: str, param: dict[str, Any] = None) -> list[dict[str, Any]]:
        """执行SQL查询"""

    @abstractmethod
    def query_for_df(self, sql: str, param: dict[str, Any] = None) -> pd.DataFrame:
        """查询返回pandas的DataFrame"""

    @abstractmethod
    def insert_df(self, table_name: str, record_df: pd.DataFrame):
        """执行数据插入"""

    @abstractmethod
    def execute(self, sql: str, param: dict[str, Any] = None) -> Any:
        """执行SQL"""
