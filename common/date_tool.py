from datetime import datetime


def timestamp_to_string():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def timestamp():
    return datetime.now()
