from config import DBNAME
from database import sqlite3db
from functions import config_functions
from dearpygui import core
import logging


def get_web_parameters():
    """
    Get the refresh time from the DB.
    return : int from DB
    """
    logging.info("start get_win_loss")
    iRv = config_functions.check_if_config_entry_exists("""
            SELECT COUNT(*) FROM WEB_PARAMETERS
            """)
    if iRv > 0:
        web_parameters = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM WEB_PARAMETERS
                                """)
        return web_parameters
    else:
        web_parameters = [[64, "", ""]]
    return web_parameters


def get_parameters_from_dpg():
    font_family = core.get_value("Font Family##Web")
    font_size = core.get_value("##BrowserTextSize")
    bg_image = core.get_value("##BgImage")
    return font_size, font_family, bg_image
