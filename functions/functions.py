import logging.handlers
import sys
from pathlib import Path


""" -------------------------------------------------------------------------------------------------------------------
                                                Converters
---------------------------------------------------------------------------------------------------------------------"""


def ConvertToInt(list1):
    """
    Convert String into Int
    return : an Integer
    """
    logging.info("start ConvertToInt")
    strings = [str(integer) for integer in list1]
    a_string = "".join(strings)
    an_integer = int(a_string)
    return an_integer


def ConvertToFloat(list1):
    """
    Convert String into Float
    return : an Float
    """
    logging.info("start ConvertToFloat")
    strings = [str(flo) for flo in list1]
    a_string = "".join(strings)
    an_float = float(a_string)
    return an_float


def listToStringWithoutBracketsAndAT(list1):
    """
    Remove unused chars from List entry
    return string
    """
    logging.info("start listToStringWithoutBracketsAndAT")
    return str(list1).replace('[', '') \
        .replace(']', '') \
        .replace('(', '') \
        .replace(')', '') \
        .replace("'", '') \
        .replace('@', '') \
        .replace('<', '') \
        .replace('>', '') \
        .replace(',', '') \
        .replace(' ', '')


def init_logger(name: str):
    if not Path("logs").exists():
        Path("logs").mkdir()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    hldr = logging.handlers.TimedRotatingFileHandler(
        "logs/{}.log".format(name), when="W0", encoding="utf-8", backupCount=16
    )
    fmt = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d]\t[%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    hldr.setFormatter(fmt)
    logger.addHandler(hldr)
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(fmt)
    stream.setLevel(logging.DEBUG)
    logger.addHandler(stream)