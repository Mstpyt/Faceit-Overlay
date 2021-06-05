""" -------------------------------------------------------------------------------------------------------------------
                                            REFRESH HANDLING
---------------------------------------------------------------------------------------------------------------------"""
from dearpygui import core

from config import DBNAME
from database import sqlite3db
from guiHandling.animationHandler import animation_config_color
from guiHandling.errorHandler import set_error


def save_refresh_time():
    """
    Saving the COL_List into the Database
    if there is already a entry into the database the entry will be updated
    """
    refresh = core.get_value("##RefreshTime")

    if int(refresh) < 5:
        animation_config_color()
        set_error("Refresh time can not be ")
    sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_REFRESH SET REFRESH = ?
                            """, refresh)
    animation_config_color()


def refresh_symbol():
    sign = core.get_value("Refresh Symbol##RefreshTime")
    sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_REFRESH_SIGN SET REFRESH_SIGN = ?
                            """, str(sign))
