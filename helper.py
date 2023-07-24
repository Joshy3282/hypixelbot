import json
import os
from random import randint


def exist_or_create(path: str, default=None) -> None:
    """
    Creates or opens a file in a path with an optional default when creating
    :param path:
    :param default:
    :return:
    """
    if not os.path.isfile(path):
        with open(path, "w") as fp:
            if default is not None:
                if type(default) is dict:
                    json.dump(default, fp)
                else:
                    fp.write(default)
    else:
        if not os.access(path, os.R_OK):
            raise Exception("File perm denied!")


def write_lines_txt(path: str, data: list, add_config_dir: bool = True) -> None:
    """
    Writes to a text file in a given path with a list. Put in config/ if True
    :param path:
    :param data:
    :param add_config_dir:
    :return:
    """
    path = "config/" + path if add_config_dir else path
    path += ".txt"
    exist_or_create(path, "")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines("\n".join(data))


def read_lines_txt(path: str, add_config_dir: bool = True) -> list:
    """
    Reads from a text file in a given path. Read from config/ if True
    :param path:
    :param add_config_dir:
    :return:
    """
    path = "config/" + path if add_config_dir else path
    path += ".txt"
    exist_or_create(path, "")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read()
    return lines.split("\n")


def write_json(path: str, data, add_config_dir: bool = True):
    """
    Writes to a json file in a given path. Put in config/ if True
    :param path:
    :param data:
    :param add_config_dir:
    :return:
    """
    path = "config/" + path if add_config_dir else path
    path += ".json"
    exist_or_create(path, {})
    with open(path, "w") as data_file:
        json.dump(data, data_file)


def load_json(path: str, add_config_dir: bool = True):
    """
    Loads a json file from a given path. Loaded from config/ if True
    :param path:
    :param add_config_dir:
    :return:
    """
    path = "config/" + path if add_config_dir else path
    path += ".json"
    exist_or_create(path, {})
    with open(path, "r") as data_file:
        data = json.load(data_file)
    return data


def randomColor() -> int:
    """
    Returns a random hex value
    :return:
    """
    return randint(0, 0xFFFFFF)


def sec2hour(seconds) -> str:
    """
    Converts seconds to hours and minutes
    :param seconds:
    :return:
    """
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d hours %02d mins" % (hour, minutes)


def sec2day(sec: int, spaced: bool = True) -> str:
    """
    Converts seconds to days hours minutes and seconds and is spaced apart if True
    :param sec:
    :param spaced:
    :return:
    """
    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    seconds = sec
    send = (
        str(int(day))
        + "dy "
        + str(int(hour))
        + "hr "
        + str(int(minutes))
        + "min "
        + str(int(seconds))
        + "sec"
    )
    return send if spaced else send.replace(" ", "")

def format_large_number(number):
    if abs(number) >= 1_000_000_000_000:  # Trillion or more
        return f'{number / 1_000_000_000_000:.2f}T'
    elif abs(number) >= 1_000_000_000:  # Billion or more
        return f'{number / 1_000_000_000:.2f}B'
    elif abs(number) >= 1_000_000:  # Million or more
        return f'{number / 1_000_000:.2f}M'
    elif abs(number) >= 1_000:  # Thousand or more
        return f'{number / 1_000:.2f}K'
    else:
        return str(number)  # Less than a thousand, no suffix