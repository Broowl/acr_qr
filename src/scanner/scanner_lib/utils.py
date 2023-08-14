from datetime import datetime, date


def str_to_date(value: str) -> date:
    return datetime.strptime(value, '%y-%m-%d').date()


def date_to_str(value: date) -> str:
    return value.strftime('%y-%m-%d')
