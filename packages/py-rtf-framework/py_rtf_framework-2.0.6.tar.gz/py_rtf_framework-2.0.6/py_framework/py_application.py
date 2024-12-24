from typing import Self, Callable
from py_framework.context.application_context import ApplicationContext, set_default_application_context
from py_framework.py_constants import APP_ROOT_DIR_ENV_KEY
import os
from py_framework.web.web_server import start_server
import importlib
import importlib.util
import pkgutil
from pathlib import Path
from types import ModuleType
import inspect
from py_framework.config.app_environment import AppEnvironment
from py_framework.log.application_log import start_log
from py_framework.schedule.job_scheduler import start_schedule
import logging

logger = logging.getLogger(__name__)


def load_py_module(module: ModuleType, is_root: bool = False) -> None:
    """加载py模块"""
    if module.__file__ is None:
        logger.info("不主动加载任何模块")
        return

    module_path = Path(module.__file__).parent

    module_name = '' if is_root else module.__name__
    for _, sub_module, is_module in pkgutil.iter_modules([str(module_path)]):
        if not is_module:
            full_path = Path(module_path) / f"{sub_module}.py"
            module_spec = importlib.util.spec_from_file_location(
                module_name, str(full_path)
            )
            if module_spec is not None:
                # module_to_load = f"{sub_module}" if module_name == '' else f"{module_spec.name}.{sub_module}" or module_spec.parent == ''
                module_to_load = f"{sub_module}" if module_name == '' else f"{module_spec.name}.{sub_module}"
                try:
                    importlib.import_module(module_to_load)
                except Exception:
                    logger.exception('加载模块' + module_to_load + '(' + str(full_path) + ')异常。', exc_info=True)
        else:
            sub_module_name = f"{sub_module}" if module_name == '' else f"{module_name}.{sub_module}"
            sub_module_rec = importlib.import_module(sub_module_name)
            load_py_module(sub_module_rec)


class PyApplication:
    """python应用初始化"""

    """是否启动Web"""
    _enable_web: bool = False

    """应用运行的根目录"""
    _root_dir: str = None

    module_list: list[ModuleType] = None

    fn_list: list[Callable] = None

    def module_scans(self: Self, module_list: list[ModuleType]) -> Self:
        """扫描模块，适用于带有注解的函数"""
        self.module_list = module_list
        return self

    def root_dir(self: Self, work_dir: str) -> Self:
        """应用根目录"""
        self._root_dir = work_dir if work_dir.endswith('/') else work_dir + '/'
        return self

    def run_fn(self: Self, _fn_list: list[Callable]) -> Self:
        """运行函数列表"""
        for _fn in _fn_list:
            arg_specs = inspect.getfullargspec(_fn)
            if len(arg_specs.args) > 0:
                error_text = f"初始运行函数必须是无参函数"
                raise ValueError(error_text)
        self.fn_list = _fn_list
        return self

    def enable_web(self: Self, start_web: bool = True) -> Self:
        """是否启用web服务"""
        self._enable_web = start_web
        return self

    def start(self) -> None:
        """开始运行"""
        # 校验根目录
        if self._root_dir is None:
            self.root_dir(os.getenv(APP_ROOT_DIR_ENV_KEY))

        application_context = ApplicationContext()

        # 1. 加载配置
        set_default_application_context(application_context)
        application_context.app_environment = AppEnvironment(base_dir=os.getcwd())

        # 2. 初始化日志
        start_log()

        logger.info('应用目录:%s', self._root_dir)

        # 3. 模块列表
        for module in self.module_list:
            load_py_module(module, True)

        # 4. 运行函数
        if self.fn_list is not None:
            for fn in self.fn_list:
                fn()

        # 5. 定时任务
        start_schedule()

        # 6. 开启web
        app_server = None
        if self._enable_web:
            app_server = start_server()

        return application_context, app_server
