from abc import ABC, abstractmethod
from typing import Any
import os
import yaml
import re


def render_env_constructor(loader, node):
    """渲染环境变量的值"""
    value = loader.construct_scalar(node)
    value_name = str(value).strip('${}')
    if value_name.find(":") != -1:
        var_name = value_name[0:value_name.find(":")].strip()
        default_value = value_name[value_name.find(":") + 1:].strip()
    else:
        var_name = value_name
        default_value = None

    target_value = os.getenv(var_name) if os.getenv(var_name) is not None else default_value

    return target_value


# 添加对环境变量的解析
yaml.SafeLoader.add_constructor('!env', render_env_constructor)
yaml.SafeLoader.add_implicit_resolver('!env', re.compile('\${(\S|\s)+}'), None)


class BaseConfigResolver(ABC):
    """基础配置解析器"""

    config: dict[str, Any]

    name: str = None

    def __init__(self, name: str):
        self.name = name
        self.config = {}

    @abstractmethod
    def load_config(self):
        """装载指定类型的配置"""

    def load_config_from_yml(self, config_file_path: str):
        """从yml中加载文件"""
        # 校验配置是否存在
        if not os.path.exists(config_file_path):
            raise ValueError(config_file_path + '不存在')

        with open(config_file_path, 'r', encoding='utf-8') as file:
            yml_config = yaml.safe_load(file)
        # 添加配置文件
        for key, value in yml_config.items():
            self.config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置属性值"""
        level_config = self.config
        # 逐层获取配置属性值
        key_items = key.split('.')
        for index, key_item in enumerate(key_items):
            if key_item in level_config:
                level_config = level_config[key_item]
            else:
                level_config = None
                break

        return level_config if level_config is not None else default

    def contain_key(self, key: str) -> bool:
        """是否存在指定属性的配置项"""
        return key in self.config
