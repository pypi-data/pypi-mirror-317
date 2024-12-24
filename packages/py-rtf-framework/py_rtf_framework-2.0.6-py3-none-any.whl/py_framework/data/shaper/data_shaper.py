from pandas import DataFrame
import json
import os
from py_framework.data.shaper.workflow import Workflow
import pandas as pd


def run_data_shaper(work_flow_schema_path: str, input_dataframe: pd.DataFrame | None = None) -> DataFrame:
    """加载配置文件中WorkFlow的schema"""

    if not os.path.exists(work_flow_schema_path):
        raise ValueError(work_flow_schema_path + '不存在')

    with open(work_flow_schema_path, 'r', encoding='utf-8') as json_file:
        workflow_schema = json.load(json_file)

    work_flow = Workflow(schema=workflow_schema, input_tables=input_dataframe)

    work_flow_result_df: DataFrame = work_flow.run_until_complete()

    return work_flow_result_df
