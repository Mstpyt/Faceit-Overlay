from dearpygui import core, simple
from dearpygui.core import mvGuiCol_Button, mvGuiCol_ButtonActive, mvGuiCol_ButtonHovered

from functions import config_functions

""" -------------------------------------------------------------------------------------------------------------------
                                            ERROR / WARNING HANDLING
---------------------------------------------------------------------------------------------------------------------"""


def set_warning(warningTxt):
    """
    Warning handling ; set
    add a collapsing_header to display the Warning Message
    """
    if not core.does_item_exist("Warning##Warning"):
        with simple.collapsing_header("Warning##Warning", parent="##GroupStats",
                                      default_open=True,
                                      closable=False,
                                      bullet=True):
            core.add_text("Warning", default_value=warningTxt, color=(255, 255, 0, 255))


def set_error(errTxt):
    """
    Error handling ; set
    set the defined Button to Red
    add a collapsing_header to display the Error Message
    """
    core.set_item_color("Start", mvGuiCol_Button, (255, 0, 0, 255))
    core.set_item_color("Start", mvGuiCol_ButtonActive, (255, 0, 0, 255))
    core.set_item_color("Start", mvGuiCol_ButtonHovered, (255, 0, 0, 255))
    if not core.does_item_exist("Error##ErrorNoFACEITName"):
        with simple.collapsing_header("Error##ErrorNoFACEITName", parent="##GroupStats",
                                      default_open=True,
                                      closable=False,
                                      bullet=True):
            core.add_text("ErrorText", default_value=errTxt, color=(255, 0, 0, 255))


def reset_error(itemtodelete):
    """
    Error handling ; reset
    set the defined Button back to the configured color
    delete the collapsing_header if needed
    """
    core.delete_item(itemtodelete)
    colors = config_functions.get_color()
    core.set_item_color("Start", mvGuiCol_Button, (colors[0][0], colors[0][1], colors[0][2], colors[0][3]))
    core.set_item_color("Start", mvGuiCol_ButtonActive, (colors[2][0], colors[2][1], colors[2][2], colors[0][3]))
    core.set_item_color("Start", mvGuiCol_ButtonHovered, (colors[0][0], colors[0][1], colors[0][2], colors[0][3]))


def delete_error():
    """
    Error handling ; delete
    delete error/warning messages
    call reset_error to set the COL_List back
    """
    item = core.get_all_items()
    for i in item:
        if "Error" in i or "Warning" in i:
            if core.does_item_exist(i):
                reset_error(i)
