from time import sleep
from dearpygui import core
import logging
import math

""" -------------------------------------------------------------------------------------------------------------------
                                            Animation open Close config
---------------------------------------------------------------------------------------------------------------------"""


def animation_config_color():
    i = 0
    logging.info("start animation config_color")
    conf = core.get_item_configuration("##Config")
    helper = core.get_item_configuration("##Help")
    if helper["show"] is True:
        core.configure_item("##Help", show=False)
        core.configure_item("##Config_Colors", show=True)
        core.configure_item("##Web", show=False)
        return
    if conf["width"] < 350:
        core.configure_item("##Config_Colors", show=True)
        core.configure_item("##Help", show=False)
        core.configure_item("##Web", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=380 + x_pos)
            sleep(0.001)
    else:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=False)
        core.configure_item("##Web", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=60 - x_pos)
            sleep(0.001)
    logging.info("end animation config_color")


def animation_config_help():
    logging.info("start animation config_help")
    i = 0
    helper = core.get_item_configuration("##Config")
    conf = core.get_item_configuration("##Config_Colors")
    if conf["show"] is True:
        core.configure_item("##Help", show=True)
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Web", show=False)
        return
    if helper["width"] < 350:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Web", show=False)
        core.configure_item("##Help", show=True)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=380 + x_pos)
            sleep(0.001)
    else:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=False)
        core.configure_item("##Web", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=60 - x_pos)
            sleep(0.001)
    logging.info("end animation config_help")


def animation_config_web():
    logging.info("start animation config_web")
    i = 0
    web = core.get_item_configuration("##Config")
    conf = core.get_item_configuration("##Config_Colors")
    if conf["show"] is True:
        core.configure_item("##Web", show=True)
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=False)
    if web["width"] < 350:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Web", show=True)
        core.configure_item("##Help", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=380 + x_pos)
            sleep(0.001)
    else:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Web", show=False)
        core.configure_item("##Help", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * 50)
            i += 0.03
            core.configure_item("##Config", x_pos=0, width=60 - x_pos)
            sleep(0.001)
    logging.info("end animation config_web")
