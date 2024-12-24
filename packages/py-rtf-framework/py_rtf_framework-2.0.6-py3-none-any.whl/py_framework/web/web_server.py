from pydantic import BaseModel, Field
from py_framework.context.application_context import get_config_dict_by_prefix, is_dev_environment
from py_framework.py_constants import APPLICATION_WEB_CONFIG_KEY
from py_framework.web.request_mapping import registered_urls
import logging

logger = logging.getLogger(__name__)


class WebServerConfig(BaseModel):
    """web服务配置"""
    port: int = Field(title="端口", default=8080)
    context_path: str = Field(title="上下文路径", default='/')


def start_server():
    """启动web服务"""
    # 1. 获取配置
    web_config_props = get_config_dict_by_prefix(APPLICATION_WEB_CONFIG_KEY, False)

    web_server_config = WebServerConfig(**web_config_props)

    # 2. 构建服务
    app_web = flask.Flask('app web服务')
    for index, app_url in enumerate(registered_urls):
        full_url = web_server_config.context_path.removesuffix('/') + '/' + app_url.path.removeprefix('/')
        app_web.add_url_rule(rule=full_url,
                             view_func=app_url.handler,
                             methods=app_url.methods,
                             endpoint=app_url.path)
        logger.info('发布服务：%s', full_url)

    # 3. 如果是开发环境，则启动服务
    if is_dev_environment():
        app_web.run(host='0.0.0.0', port=web_server_config.port, debug=False)

    return app_web
