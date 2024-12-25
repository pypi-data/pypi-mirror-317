from .base_jdbc_template import BaseJdbcTemplate, DbConfig, DbType
from py_framework.context.application_context import get_config_dict_by_prefix
from py_framework.data.jdbc.mysql_jdbc_template import MysqlJdbcTemplate
from py_framework.data.jdbc.clickhouse_jdbc_template import ClickhouseJdbcTemplate
import logging

logger = logging.getLogger(__name__)


def jdbc_template_from_config(config_prefix: str) -> BaseJdbcTemplate:
    """获取mysql的操作模板"""
    config_props = get_config_dict_by_prefix(config_prefix)

    db_config = DbConfig(**config_props)
    logger.info('%s连接配置: %s', config_prefix, db_config.json())
    if db_config.type is None:
        raise ValueError('数据库类型不能为空')

    if db_config.type == DbType.MySql:
        jdbc_template = MysqlJdbcTemplate(db_config)
    elif db_config.type == DbType.ClickHouse:
        jdbc_template = ClickhouseJdbcTemplate(db_config)
    else:
        raise ValueError('不支持' + db_config.type + "创建jdbcTemplate")

    return jdbc_template
