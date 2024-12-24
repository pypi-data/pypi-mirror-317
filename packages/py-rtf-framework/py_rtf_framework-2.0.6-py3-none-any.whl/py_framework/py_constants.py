from enum import Enum

"""应用根目录在环境变量中的参数"""
APP_ROOT_DIR_ENV_KEY = 'py_framework_root_dir'

APPLICATION_WEB_CONFIG_KEY = "application.web"

APPLICATION_LOG_CONFIG_KEY = "application.log"

APPLICATION_NAME = "application.name"

APPLICATION_PROFILE = "application.profile"


class AppProfile(str, Enum):
    """系统运行环境"""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"
