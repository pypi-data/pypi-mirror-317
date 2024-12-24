from .base_config_resolver import BaseConfigResolver
import os


class EnvConfigResolver(BaseConfigResolver):
    """环境配置解析器"""

    def __init__(self):
        super().__init__('environment')

    def load_config(self):
        for key, value in os.environ.items():
            self.config[key] = value
