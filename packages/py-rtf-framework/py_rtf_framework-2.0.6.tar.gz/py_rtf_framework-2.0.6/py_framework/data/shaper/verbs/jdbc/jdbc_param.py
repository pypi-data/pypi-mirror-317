from datetime import datetime, timedelta


def default_params() -> dict[str, str]:
    params = {
        'sys_date': datetime.now().strftime('%Y-%m-%d'),
        'sys_datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sys_datetime_min': datetime.now().strftime('%Y-%m-%d 00:00:00'),
        'sys_datetime_max': datetime.now().strftime('%Y-%m-%d 23:59:59'),
        'last_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'last_datetime': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        'last_datetime_min': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'),
        'last_datetime_max': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 23:59:59'),
    }

    return params
