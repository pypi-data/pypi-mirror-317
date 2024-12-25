from typing import Any

import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.data.jdbc.jdbc_template import DbType, jdbc_template_from_config
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate


@verb(
    name="jdbc_insert",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def jdbc_insert(
        table: pd.DataFrame,
        insert_table: str,
        insert_columns: list[str] = None,
        db_config_prefix: str = None,
        **_kwargs: Any,
) -> pd.DataFrame:
    jdbc_template: BaseJdbcTemplate = jdbc_template_from_config(config_prefix=db_config_prefix)

    # 插入的列
    if insert_columns is None:
        record_df = table
    else:
        record_df = table[insert_columns]

    jdbc_template.insert_df(table_name=insert_table, record_df=record_df)

    return table
