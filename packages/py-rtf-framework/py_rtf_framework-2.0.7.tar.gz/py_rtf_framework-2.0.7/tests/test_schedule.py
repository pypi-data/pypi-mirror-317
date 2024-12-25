from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from datetime import datetime


def my_job():
    print('cron任务执行:', datetime.now())


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    cron_exp = '10 47 14 * * ?'
    cron_parts = cron_exp.split(' ')
    print('---------', cron_parts)
    scheduler.add_job(my_job, 'cron', second=cron_parts[0], minute=cron_parts[1], hour=cron_parts[2],
                      day=cron_parts[3], month=cron_parts[4])
    scheduler.start()
    input()
