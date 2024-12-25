from .base_config_resolver import BaseConfigResolver
from py_framework.py_constants import AppProfile
import logging

logger = logging.getLogger(__name__)


class ApplicationConfigResolver(BaseConfigResolver):
    """启动配置解析器"""
    base_dir: str

    profile: AppProfile

    def __init__(self, profile: AppProfile, base_dir: str = './'):
        super().__init__('application')
        self.base_dir = base_dir if base_dir.endswith('/') else base_dir + '/'
        self.profile = profile
        # 开始装载配置
        self.load_config()

    def load_config(self):
        logger.info("加载配置文件: %s", self.base_dir + 'application-' + self.profile + '.yml')
        self.load_config_from_yml(self.base_dir + 'application-' + self.profile + '.yml')
