import pandas as pd
from py_framework.data.shaper.verbs.decorators import OutputMode, inputs, outputs, verb
from typing import Any, List
from py_framework.context.application_context import get_config_dict_by_prefix
from tqdm import tqdm
from aiolimiter import AsyncLimiter
import logging

logger = logging.getLogger(__name__)


@verb(
    name="llm_prompt",
    adapters=[
        inputs(default_input_argname="table"),
        outputs(mode=OutputMode.Table),
    ],
)
async def llm_prompt(
        table: pd.DataFrame,
        prompt_template: str,
        prompt_variables: list[str],
        model_column: str = 'llm_model_value',
        llm_model_config_key: str = 'tongyi',
        **_kwargs: Any,
) -> pd.DataFrame:
    # 执行prompt文本替换
    prompt_template = langchain_core.prompts.PromptTemplate.from_template(prompt_template)

    prompt_text_list = [prompt_template.format(**variable) for variable in table[prompt_variables].to_dict('records')]

    if llm_model_config_key == 'tongyi':
        prompt_values = await tongyi_model_invoke(prompt_text_list)
    else:
        raise ValueError('不支持llm model类型：' + llm_model_config_key)

    # 添加新的列
    table[model_column] = prompt_values

    return table


async def tongyi_model_invoke(prompt_text_list: List[str]) -> List[str]:
    """执行通义千问模型"""
    # 获取llm的配置
    llm_model_config = get_config_dict_by_prefix('application.llm.model.tongyi')

    logger.debug("tongyi配置: %s", llm_model_config)

    tongyi = langchain_community.llms.tongyi.Tongyi(model_name=llm_model_config['model_name'],
                    dashscope_api_key=llm_model_config['api_key'])

    # 对tongyi请求进行限流
    rate_limit = AsyncLimiter(50, 60)

    model_values = []
    for prompt_text in tqdm(prompt_text_list, desc='llm model'):
        # 限流等待
        await rate_limit.acquire(1)
        model_value = ''
        try:
            model_value = tongyi.invoke(prompt_text)
            model_values.append(model_value)
        except Exception as e:
            logger.exception("调用tongyi异常", exc_info=True)
            model_values.append('')
        logger.debug("调用tongyi，prompt_text: %s , 结果: %s", prompt_text, model_value)

    return model_values
