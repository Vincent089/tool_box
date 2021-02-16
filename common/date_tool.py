from datetime import datetime


def timestamp_to_string():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def timestamp():
    return datetime.now()


def current_text_month():
    return datetime.now().strftime('%h')


def current_text_year():
    return datetime.now().strftime('%Y')
