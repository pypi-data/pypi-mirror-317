import os
import sys
from py_framework.py_constants import APP_ROOT_DIR_ENV_KEY
from py_framework.py_application import load_py_module


def _load_root_dir():
    """加载模块"""
    _root_dir = __path__[0]
    os.environ[APP_ROOT_DIR_ENV_KEY] = _root_dir


def _init_app():
    """初始化应用"""
    _load_root_dir()
    load_py_module(sys.modules[__name__])


_init_app()
