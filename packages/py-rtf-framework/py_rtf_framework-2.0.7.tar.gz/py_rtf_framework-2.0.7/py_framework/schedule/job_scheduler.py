from typing import Callable
import inspect
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


def scheduled(cron: str):
    """添加定时任务"""

    def add_schedule_task(job_fn: Callable):
        register_job(cron, job_fn)

    return add_schedule_task


class ScheduleJob(BaseModel):
    """调度任务"""
    name: str = Field(title="名称")
    cron: str = Field(title="cron表达式")
    task: Callable = Field(title="调度函数")

    def get_cron_parts(self):
        """获取cron中每一部分"""
        cron_parts = self.cron.split(' ')
        if len(cron_parts) < 5:
            raise ValueError('cron定时任务表达式错误：' + self.cron)
        return cron_parts


# 存储注册的任务
__registered_jobs: list[ScheduleJob] = []
__registered_jobs_names: list[str] = []


def register_job(cron: str, job_fn: Callable):
    """注册定时任务"""

    if len(cron.strip()) < 1:
        raise ValueError('定时任务表达式不能为空')

    if inspect.isfunction(job_fn) is False:
        error_text = f"{cron} 定时任务必须为函数"
        raise ValueError(error_text)

    raw_handler_arg_specs = inspect.getfullargspec(job_fn)
    if len(raw_handler_arg_specs.args) > 0:
        error_text = f"{cron} 定时任务函数参数必须为空"
        raise ValueError(error_text)

    # 获取函数名称
    register_name = str(job_fn)

    if register_name in __registered_jobs_names:
        logger.info('定时任务：%s 已注册', register_name)
        return

    # 存储注册任务
    __registered_jobs_names.append(register_name)
    __registered_jobs.append(ScheduleJob(name=register_name, cron=cron, task=job_fn))


# 初始化全局调度任务
scheduler = BackgroundScheduler()


def start_schedule():
    """开启调度任务"""
    for schedule_job in __registered_jobs:
        # 获取调度cron
        cron_parts = schedule_job.get_cron_parts()
        scheduler.add_job(schedule_job.task, 'cron', second=cron_parts[0], minute=cron_parts[1], hour=cron_parts[2],
                          day=cron_parts[3], month=cron_parts[4])
    scheduler.start()
