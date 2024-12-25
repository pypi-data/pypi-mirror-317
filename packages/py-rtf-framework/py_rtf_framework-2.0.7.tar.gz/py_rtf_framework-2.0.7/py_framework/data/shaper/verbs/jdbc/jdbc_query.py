from typing import Any

import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.data.jdbc.jdbc_template import jdbc_template_from_config
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate
import logging
import numpy as np
from py_framework.data.shaper.verbs.jdbc.jdbc_param import default_params

logger = logging.getLogger(__name__)


@verb(
    name="jdbc_query",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def jdbc_query(
        table: pd.DataFrame,
        query_sql: str,
        query_param: dict = None,
        input_as_param: bool = False,
        db_config_prefix: str = None,
        **_kwargs: Any,
) -> pd.DataFrame:
    jdbc_template: BaseJdbcTemplate = jdbc_template_from_config(config_prefix=db_config_prefix)

    if query_param is None:
        query_param = {}

    # 添加默认的参数
    query_param.update(default_params())

    # 是否合并table参数
    if input_as_param:
        table_params = parse_table_params(table)
        query_param.update(table_params)

    query_result_df = jdbc_template.query_for_df(query_sql, query_param)

    return query_result_df


def parse_table_params(table: pd.DataFrame) -> dict[str, str]:
    # 原始数据为空，返回空数据
    if table is None or len(table) < 1:
        return {}
    table_param = {}
    # 转换字典列表
    column_dict = table.to_dict('list')
    for column in column_dict.items():
        param_name = column[0]
        # 如果值个数大于1，在默认使用()格式，否则使用单值
        if len(column[1]) > 1:
            unique_values = np.unique(np.array(column[1]))
            param_value = ','.join(["'" + str(v) + "'" for v in unique_values])
        elif len(column[1]) > 0:
            param_value = "'" + str(column[1]) + "'"
        else:
            param_value = ''

        table_param[param_name] = param_value

    return table_param
