""" -------------------------------------------------------------------------------------------------------------------
                                            SIZE HANDLING
---------------------------------------------------------------------------------------------------------------------"""
from dearpygui import core

from config import DBNAME
from database import sqlite3db
from functions import config_functions
from guiHandling.animationHandler import animation_config_color


def save_scale():
    """
    Saving the COL_List into the Database
    if there is already a entry into the database the entry will be updated
    """
    iRv = config_functions.check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_SCALE
            """)
    scale = core.get_global_font_scale()
    if iRv > 0:
        sqlite3db.TExecSql(DBNAME, """
                                UPDATE CFG_SCALE SET Scale = ?
                                """, scale)

    else:
        sqlite3db.TExecSql(DBNAME,
                           """
                                 INSERT INTO CFG_SCALE
                                 VALUES (?)
                                 """, scale
                           )
    animation_config_color()


def reset_scale():
    """
    Saving the COL_List into the Database
    if there is already a entry into the database the entry will be updated
    """
    core.set_value("Global Scale", 1.0)
    core.set_global_font_scale(1.0)
