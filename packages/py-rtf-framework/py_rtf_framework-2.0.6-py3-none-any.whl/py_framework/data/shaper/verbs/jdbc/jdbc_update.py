from typing import Any

import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from py_framework.data.jdbc.jdbc_template import DbType, jdbc_template_from_config
from py_framework.data.jdbc.base_jdbc_template import BaseJdbcTemplate
from tqdm import tqdm


@verb(
    name="jdbc_update",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
def jdbc_update(
        table: pd.DataFrame,
        update_template: str,
        db_config_prefix: str = None,
        **_kwargs: Any,
) -> pd.DataFrame:
    jdbc_template: BaseJdbcTemplate = jdbc_template_from_config(config_prefix=db_config_prefix)

    update_template_text = langchain_core.prompts.PromptTemplate.from_template(update_template)

    update_sql_list = [update_template_text.format(**variable) for variable in table.to_dict('records')]

    if len(update_sql_list) > 0:
        for update_sql in tqdm(update_sql_list, desc="jdbc_update"):
            jdbc_template.execute(sql=update_sql)

    return table
