from py_framework.config.bootstrap_config_resolver import BootstrapConfigResolver
from py_framework.config.application_config_resolver import ApplicationConfigResolver
from py_framework.config.env_config_resolver import EnvConfigResolver
from py_framework.config.base_config_resolver import BaseConfigResolver
from typing import Any
from pydantic import BaseModel, Field
from py_framework.py_constants import APPLICATION_NAME, APPLICATION_PROFILE
from py_framework.py_constants import AppProfile
import logging

logger = logging.getLogger(__name__)


class AppBootstrap(BaseModel):
    """应用bootstrap配置"""

    name: str = Field(default='应用名称', title="系统名称")
    profile: AppProfile = Field(default=AppProfile.DEV, title="系统运行环境")

    @staticmethod
    def from_config(config_resolver: BaseConfigResolver):
        app_bootstrap = AppBootstrap(name=config_resolver.get_config(APPLICATION_NAME, ''),
                                     profile=config_resolver.get_config(APPLICATION_PROFILE, AppProfile.DEV))
        return app_bootstrap


class AppEnvironment:
    """应用环境"""
    app_bootstrap: AppBootstrap

    bootstrap_config: BaseConfigResolver

    env_config: BaseConfigResolver

    application_config: BaseConfigResolver

    base_dir: str

    config_list: list[BaseConfigResolver]

    def __init__(self, base_dir: str = './'):
        self.base_dir = base_dir if base_dir.endswith('/') else base_dir + '/'
        # 装载bootstrap配置
        self.bootstrap_config = BootstrapConfigResolver(self.base_dir)
        self.app_bootstrap = AppBootstrap.from_config(self.bootstrap_config)
        logger.info("当前环境：%s", self.app_bootstrap.profile.value)
        # 装载应用配置
        self.application_config = ApplicationConfigResolver(self.app_bootstrap.profile, self.base_dir)
        # 装载环境配置
        self.env_config = EnvConfigResolver()
        # 完整环境配置
        self.config_list = [self.bootstrap_config, self.application_config, self.env_config]

    def get_config(self, key: str, default: Any = None) -> Any:
        config_value = None
        # 按照优先级获取配置
        for config_source in self.config_list:
            config_value = config_source.get_config(key)
            if config_value is not None:
                break
        # 如果有值则使用配置的值，否则返回默认值
        return config_value if config_value is not None else default

    def contain_key(self, key: str) -> bool:
        return self.get_config(key) is not None
