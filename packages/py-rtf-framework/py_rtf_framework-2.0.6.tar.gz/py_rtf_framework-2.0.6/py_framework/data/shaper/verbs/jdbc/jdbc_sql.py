from typing import Any

import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.data.jdbc.jdbc_template import DbType, jdbc_template_from_config
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate
from tqdm import tqdm


@verb(
    name="jdbc_sql",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def jdbc_sql(
        table: pd.DataFrame,
        sql: str = None,
        sqls: list[str] = None,
        db_config_prefix: str = None,
        **_kwargs: Any,
) -> pd.DataFrame:
    jdbc_template: BaseJdbcTemplate = jdbc_template_from_config(config_prefix=db_config_prefix)

    if sql is not None:
        jdbc_template.execute(sql=sql)

    if sqls is not None:
        for sql_text in tqdm(sqls, desc='jdbc_sql'):
            jdbc_template.execute(sql=sql_text)

    return table
