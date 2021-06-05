""" -------------------------------------------------------------------------------------------------------------------
                                            WEB HANDLING
---------------------------------------------------------------------------------------------------------------------"""
import logging

from dearpygui import core

from config import DBNAME
from database import sqlite3db
from functions import config_functions


def save_web():
    """
    """
    web_only = core.get_value("Open in Browser Only##Browser")
    web_app = core.get_value("Open in Browser and App##Browser")
    web_update = web_only, web_app
    sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_WEB SET WEB_ONLY = ?,
                            WEB_APP = ?
                            """, web_update)


def save_font():
    logging.info("Start save_font")
    font_family = core.get_value("Font Family##Web")
    font_size = core.get_value("##BrowserTextSize")
    bg_image = core.get_value("##BgImage")
    upd = font_size, font_family, bg_image
    iRv = config_functions.check_if_config_entry_exists("""
            SELECT COUNT(*) FROM WEB_PARAMETERS
            """)
    if iRv > 0:
        sqlite3db.TExecSql(DBNAME, """
                                UPDATE WEB_PARAMETERS SET FONT_SIZE = ?,
                                FONT_FAMILY = ?,
                                BG_IMAGE = ?
                                """, upd)
    else:
        sqlite3db.TExecSql(DBNAME, """
                        INSERT INTO WEB_PARAMETERS
                        VALUES (?,?,?)""", upd)
