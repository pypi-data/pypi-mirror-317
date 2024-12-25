from typing import Any
import re
import logging

logger = logging.getLogger(__name__)


def format_sql(text_sql: str, param: dict[str, Any]) -> str:
    """格式化SQL返回格式化后的字符串"""
    if param is None:
        return text_sql
    # 执行SQL替换
    for param_name in param.keys():
        # 将结果转换为字符串
        if param[param_name] is None:
            continue
        param_value = str(param[param_name])
        # 直接替换
        param_pattern_1 = re.compile(r'\${' + param_name + '}')
        text_sql = param_pattern_1.sub(param_value, text_sql)
        # 使用引号替换
        param_pattern_2 = re.compile(r'#{' + param_name + '}')
        text_sql = param_pattern_2.sub("'" + param_value + "'", text_sql)

    logger.info("格式化sql:%s", text_sql)

    return text_sql

# if __name__ == '__main__':
#     text_sql = "select * from table_name where id = #{id} "
#     result_sql = format_sql(text_sql, {'id': 1})
#     print(result_sql)
