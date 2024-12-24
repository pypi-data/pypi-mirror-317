from typing import Any
from py_framework.config.app_environment import AppEnvironment, AppBootstrap
from py_framework.py_constants import AppProfile


class ApplicationContext:
    """应用配置上下文"""
    app_environment: AppEnvironment


# 全局应用上下文
default_application_context: ApplicationContext


def set_default_application_context(_application_context: ApplicationContext):
    """设置默认上下文"""
    global default_application_context
    default_application_context = _application_context


def get_config_dict_by_prefix(config_prefix: str, required: bool = True) -> dict[str, Any]:
    """从应用配置中，根据配置前缀获取配置属性dict。如果是必填，配置数据为空，则抛出异常。"""
    if default_application_context is None:
        raise ValueError(f"应用上下文对象ApplicationContext为空，请先执行bootstrap初始化")

    config_props = default_application_context.app_environment.get_config(config_prefix)
    if config_props is None and required:
        error_text = f"配置前缀：{config_prefix} 下找不到配置"
        raise ValueError(error_text)

    return config_props or {}


def get_config_value_by_key(config_key: str, default_value: Any | None = None) -> Any:
    """从应用配置中，根据配置Key获取配置属性值"""
    if default_application_context is None:
        raise ValueError(f"应用上下文对象ApplicationContext为空，请先执行bootstrap初始化")

    config_prop = default_application_context.app_environment.get_config(config_key)

    return config_prop or default_value


def is_dev_environment() -> bool:
    """是否为开发环境"""
    app_bootstrap: AppBootstrap = default_application_context.app_environment.app_bootstrap

    return app_bootstrap.profile == AppProfile.DEV
