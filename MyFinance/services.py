from datetime import datetime, timedelta


def create_formatted_datetime(start: str, end: str) -> tuple:
    """ Форматиреует полученные значения datetime из запроса и переводит в utc,
        если они отсутствуют, то устанавливает значения по умолчанию
    """
    if not start:
        start_date = datetime.today().replace(day=1) + timedelta(hours=2)
    else:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
    if not end:
        end_date = datetime.now() + timedelta(hours=2)
    else:
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)

    return start_date, end_date


def get_formatted_datetime(start: str, end: str) -> tuple:
    """ Форматиреует полученные значения datetime из запроса и переводит в utc если они присутствуют
    """
    start_date = None
    end_date = None

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)
    if end:
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=2)

    return start_date, end_date
