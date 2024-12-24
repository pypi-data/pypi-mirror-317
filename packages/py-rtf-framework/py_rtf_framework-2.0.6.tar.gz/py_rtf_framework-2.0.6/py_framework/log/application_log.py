from py_framework.context.application_context import get_config_dict_by_prefix
from py_framework.py_constants import APPLICATION_LOG_CONFIG_KEY
from pydantic import BaseModel, Field
from enum import Enum
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from typing import Any


class AppLogLevel(str, Enum):
    """日志级别"""

    DEBUG = "debug"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


class AppLogConfig(BaseModel):
    """日志配置"""

    level: AppLogLevel = Field(default=AppLogLevel.INFO, title="日志级别")

    log_folder: str = Field(default='./logs', title="日志文件夹")

    log_file: str = Field(default='py-logfile.log', title="日志文件")

    log_time_format: str = Field(default='%Y-%m-%d %H:%M:%S', title="日志时间格式")

    log_msg_format: str = Field(
        default='%(asctime)s - %(thread)d - %(name)s - %(levelname)s - %(lineno)d - %(message)s',
        title="日志内容格式")

    def get_log_filename(self):
        """获取日志文件路径"""
        # 创建日志目录
        if not os.path.exists(self.log_folder):
            os.mkdir(self.log_folder)
        return self.log_folder + '/' + self.log_file

    def get_logging_level(self):
        """获取日志级别"""
        match self.level:
            case AppLogLevel.DEBUG:
                return logging.DEBUG

            case AppLogLevel.WARN:
                return logging.WARN

            case AppLogLevel.ERROR:
                return logging.ERROR

            case _:
                return logging.INFO

    def get_logging_format(self):
        """获取日志格式"""
        return logging.Formatter(self.log_msg_format)


class AppLog:
    """应用日志"""
    log_config: AppLogConfig

    log_levels: dict[str, Any] = {
        'apscheduler.executors.default': logging.WARN,
        'apscheduler.scheduler': logging.WARN
    }

    def __init__(self):
        log_config_dict = get_config_dict_by_prefix(APPLICATION_LOG_CONFIG_KEY, False)
        self.log_config = AppLogConfig(**log_config_dict)

    def start(self):
        """开启日志"""
        # 日志级别
        log_level = self.log_config.get_logging_level()
        log_format = self.log_config.get_logging_format()

        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)  # 标准输出sys.stdout重定向
        console_handler.setLevel(level=log_level)
        console_handler.setFormatter(log_format)

        # 单文件输出
        # FileHandler
        file_handler = logging.FileHandler(self.log_config.get_log_filename())
        file_handler.setLevel(level=log_level)
        file_handler.setFormatter(log_format)

        # 时间轮巡文件输出
        time_rotating_file = TimedRotatingFileHandler(filename=self.log_config.get_log_filename(),
                                                      when='midnight',
                                                      backupCount=14,
                                                      encoding='utf8')
        time_rotating_file.setLevel(level=log_level)
        time_rotating_file.setFormatter(log_format)

        logging.basicConfig(level=log_level,
                            datefmt=self.log_config.log_time_format,
                            handlers=[console_handler, time_rotating_file])

        for log_config in self.log_levels.items():
            logging.getLogger(log_config[0]).setLevel(log_config[1])


def start_log():
    """开启日志"""
    app_log = AppLog()
    app_log.start()
