""" -------------------------------------------------------------------------------------------------------------------
                                            COLOR HANDLING
---------------------------------------------------------------------------------------------------------------------"""
from dearpygui import core
from dearpygui.core import mvGuiCol_Button, mvGuiCol_Text, mvGuiCol_ButtonActive, mvGuiCol_ButtonHovered, \
    mvGuiCol_WindowBg, mvGuiCol_Border, mvGuiStyleVar_WindowRounding

from config import DBNAME
from database import sqlite3db
from functions import config_functions
from guiHandling.animationHandler import animation_config_color


def get_data_from_colors():
    """
    get the COL_List from the add_color_edit3 objects
    return every object single but also as list
    """
    HEADER_List = list(map(int, core.get_value("Header#Color")))
    TEXT_List = list(map(int, core.get_value("Text#Color")))
    BUT_ACTIVE_List = list(map(int, core.get_value("ButtonActive#Color")))
    BG_List = list(map(int, core.get_value("BG#Color")))
    OUTLINE_List = list(map(int, core.get_value("Outline#Color")))
    COL_List = (HEADER_List, TEXT_List, BUT_ACTIVE_List, BG_List, OUTLINE_List)
    return HEADER_List, TEXT_List, BUT_ACTIVE_List, BG_List, OUTLINE_List, COL_List


def save_colors():
    """
    Saving the COL_List into the Database
    if there is already a entry into the database the entry will be updated
    """
    iRv = config_functions.check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_COLORS
            """)
    HEADER_List, TEXT_List, BUT_ACTIVE_List, BG_List, OUTLINE_List, COL_List = get_data_from_colors()
    DBUPDATE_List = ("Header", "Text", "ButtonActive", "Background", "Outline")
    cnt = 0
    if iRv > 0:
        for x in DBUPDATE_List:
            COL_List[cnt].append(x)
            sqlite3db.TExecSql(DBNAME, """
                                    UPDATE CFG_COLORS SET Red = ?,
                                    Green = ?,
                                    Blue = ?,
                                    Trans = ?
                                    WHERE Type = ?
                                    """, COL_List[cnt])
            cnt += 1
    else:
        cnt = 0
        for x in DBUPDATE_List:
            COL_List[cnt].append(x)
            sqlite3db.TExecSql(DBNAME,
                               """
                                     INSERT INTO CFG_COLORS
                                     VALUES (?, ?, ?, ?, ?)
                                     """, COL_List[cnt]
                               )
            cnt += 1
    set_colors(COL_List)
    animation_config_color()


def set_colors(COL_List: list):
    """
    Set the Theme Colors new
    """
    core.set_theme_item(mvGuiCol_Button, COL_List[0][0], COL_List[0][1], COL_List[0][2], COL_List[0][3])
    core.set_theme_item(mvGuiCol_ButtonHovered, COL_List[0][0], COL_List[0][1], COL_List[0][2], COL_List[0][3])
    core.set_theme_item(mvGuiCol_Text, COL_List[1][0], COL_List[1][1], COL_List[1][2], COL_List[1][3])
    core.set_theme_item(mvGuiCol_ButtonActive, COL_List[2][0], COL_List[2][1], COL_List[2][2], COL_List[2][3])
    core.set_theme_item(mvGuiCol_WindowBg, COL_List[3][0], COL_List[3][1], COL_List[3][2], COL_List[3][3])
    core.set_theme_item(mvGuiCol_Border, COL_List[4][0], COL_List[4][1], COL_List[4][2], COL_List[4][3])
    core.set_item_color("##Config", mvGuiCol_Text,
                        color=(COL_List[1][0], COL_List[1][1], COL_List[1][2], COL_List[1][3]))
    core.set_item_color("##Config", mvGuiCol_WindowBg,
                        color=(COL_List[3][0], COL_List[3][1], COL_List[3][2], COL_List[3][3] - 10))
    core.set_item_style_var("##Config", mvGuiStyleVar_WindowRounding, value=[0])
    core.set_item_color("##Config", mvGuiCol_Border,
                        color=(COL_List[3][0], COL_List[3][1], COL_List[3][2], COL_List[3][3]))
    core.set_item_color("Start", mvGuiCol_Button,
                        color=(COL_List[0][0], COL_List[0][1], COL_List[0][2], COL_List[0][3]))
    core.set_item_color("Start", mvGuiCol_ButtonActive,
                        color=(COL_List[2][0], COL_List[2][1], COL_List[2][2] - 10))
    core.set_value("Header#Color", [COL_List[0][0], COL_List[0][1], COL_List[0][2], COL_List[0][3]])
    core.set_value("Text#Color", [COL_List[1][0], COL_List[1][1], COL_List[1][2], COL_List[1][3]])
    core.set_value("ButtonActive#Color", [COL_List[2][0], COL_List[2][1], COL_List[2][2], COL_List[2][3]])
    core.set_value("BG#Color", [COL_List[3][0], COL_List[3][1], COL_List[3][2], COL_List[3][3]])
    core.set_value("Outline#Color", [COL_List[4][0], COL_List[4][1], COL_List[4][2], COL_List[4][3]])


def test_colors():
    """
    Test the COL_List and don't save them into the database
    """
    header, text, butactive, background, outline, colors = get_data_from_colors()
    set_colors(colors)
    animation_config_color()


def reset_colors():
    """
    Get the COL_List saved into the database and set them
    """
    colors = config_functions.get_color()
    set_colors(colors)
