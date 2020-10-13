from datetime import datetime

FORMAT = '%Y-%m-%d %H:%M:%S'


def timestamp():
    """
    :return: str timestamp in the format of YYYY-MM-DD HH:MM:SS
    """
    return datetime.now().strftime(FORMAT)


