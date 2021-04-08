import math
from time import sleep
import win32gui
from dearpygui import core, simple
from dearpygui.core import mvGuiCol_Text, mvGuiCol_WindowBg, mvGuiCol_Button, mvGuiCol_Border, \
    mvGuiCol_ButtonActive, delete_item, mvGuiCol_ButtonHovered, mvGuiCol_BorderShadow, \
    mvGuiStyleVar_WindowRounding
from dearpygui.demo import mvGuiStyleVar_FramePadding
import eloOverlay
from config import DBNAME
from database import db_create, sqlite3db
from functions import config_functions, functions
import logging
"""
Global Values
iChanges : set if a change was made in a configuration
"""
iChanges = 0

""" -------------------------------------------------------------------------------------------------------------------
                                            GET START DATA
---------------------------------------------------------------------------------------------------------------------"""


def startup():
    """
    Get all data from the Database. If no Database entry exists, set everything on default.
    """
    logging.info("Get startup values")
    iRv = config_functions.check_if_dbfile_exists()
    FACEIT_List = []
    MATCH_List = []
    nameFACEIT = ""
    if iRv > 0:
        iRv = config_functions.check_if_config_entry_exists()
        if iRv > 0:
            list_faceit = sqlite3db.TExecSqlReadMany(DBNAME, """
                                                    SELECT * FROM CFG_STATS_FACEIT
                                                     """
                                                     )
            list_matches = sqlite3db.TExecSqlReadMany(DBNAME, """
                                                    SELECT * FROM CFG_STATS_MATCH
                                                     """
                                                      )
            nameFACEIT = config_functions.get_faceit_name_from_db()
            for i in list_faceit[0]:
                if i == str(0):
                    FACEIT_List.append(False)
                else:
                    FACEIT_List.append(True)
            for i in list_matches[0]:
                if i == str(0):
                    MATCH_List.append(False)
                else:
                    MATCH_List.append(True)
            return FACEIT_List, MATCH_List, nameFACEIT
        else:
            for x in range(0, 6):
                FACEIT_List.append(True)
            for x in range(0, 7):
                MATCH_List.append(True)
            return FACEIT_List, MATCH_List, nameFACEIT
    else:
        for x in range(0, 6):
            FACEIT_List.append(True)
        for x in range(0, 7):
            MATCH_List.append(True)
        return FACEIT_List, MATCH_List, nameFACEIT


""" -------------------------------------------------------------------------------------------------------------------
                                            APPLY CONFIGURATION
---------------------------------------------------------------------------------------------------------------------"""


def get_values_to_safe_faceit():
    """
    get all values to save and return them in different lists.
    """
    acName = core.get_value("##FaceitName")
    acElo = core.get_value("Current Elo##stats")
    acRank = core.get_value("Faceit Rank##stats")
    acEloToday = core.get_value("Elo Gained today##stats")
    acStreak = core.get_value("Win Streak##stats")
    acTotMatches = core.get_value("Total Matches##stats")
    acMatchesWon = core.get_value("Matches Won##stats")
    acScore = core.get_value("Score##match")
    acResult = core.get_value("Result (W/L)##match")
    acMap = core.get_value("Map##match")
    acKd = core.get_value("K/D##match")
    acEloDiff = core.get_value("Elo Diff##match")
    acKills = core.get_value("Kills##match")
    acDeath = core.get_value("Death##match")

    FACEIT_List = (acElo, acRank, acEloToday,
                   acStreak, acTotMatches, acMatchesWon)
    MATCH_List = (acMap, acResult, acScore, acKd, acEloDiff,
                  acKills, acDeath)
    return FACEIT_List, MATCH_List, acName


def save_data():
    """
    Save all configuration into the database. if a database already exists update the current one.
    get and set the FACEIT name. if the Name isn't correct set error
    """
    global iChanges
    iRv = config_functions.check_if_config_entry_exists()
    FACEIT_List, MATCH_List, acName = get_values_to_safe_faceit()
    name = config_functions.get_faceit_name_from_db()
    if not acName:
        set_error("Faceit Name must be set!")
        return
    if name:
        name = functions.listToStringWithoutBracketsAndAT(name[0])
        if name != acName and acName:
            sqlite3db.TExecSql(DBNAME, """
                            DELETE FROM CFG_FACEIT_NAME""")
            sqlite3db.TExecSql(DBNAME, """
                                        INSERT INTO CFG_FACEIT_NAME
                                        VALUES (? )""", acName)

    if iRv == 1:
        sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_STATS_FACEIT SET CurrentElo = ?,
                            Rank = ?,
                            EloToday = ?,
                            WinStreak = ?,
                            TotalMatches = ?,
                            MatchesWon = ?
        
        """, FACEIT_List)
        sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_STATS_MATCH SET Score = ?,
                            Result = ?,
                            Map = ?,
                            KD = ?,
                            EloDiff = ?,
                            Kills = ?,
                            Death = ?
        """, MATCH_List)
        sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_FACEIT_NAME SET Name = ?
                            """, acName)
    else:
        sqlite3db.TExecSql(DBNAME, """
                            INSERT INTO CFG_STATS_FACEIT
                            VALUES (?, ?, ?, ?, ?, ?)""", FACEIT_List)
        sqlite3db.TExecSql(DBNAME, """
                            INSERT INTO CFG_STATS_MATCH
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", MATCH_List)
        if acName:
            sqlite3db.TExecSql(DBNAME, """
                                        INSERT INTO CFG_FACEIT_NAME
                                        VALUES (? )""", acName)
    delete_error()
    COL_List = config_functions.get_color()
    core.set_item_color("Apply Configuration", mvGuiCol_Text,
                        (COL_List[1][1], COL_List[1][2], COL_List[1][3], 255))
    iRv = config_functions.check_faceit_name_api(acName)
    if iRv < 0:
        set_error("Wrong FACEIT Name")
    iChanges = 0


""" -------------------------------------------------------------------------------------------------------------------
                                            COLOR HANDLING
---------------------------------------------------------------------------------------------------------------------"""


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
    iRv = config_functions.check_if_color_config_entry_exists()
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
    colors = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT Red, Green, Blue, Trans FROM CFG_COLORS""")
    set_colors(colors)


""" -------------------------------------------------------------------------------------------------------------------
                                            SIZE HANDLING
---------------------------------------------------------------------------------------------------------------------"""


def save_scale():
    """
    Saving the COL_List into the Database
    if there is already a entry into the database the entry will be updated
    """
    iRv = config_functions.check_if_scale_config_entry_exists()
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


""" -------------------------------------------------------------------------------------------------------------------
                                            CHECKBOX HANDLING
---------------------------------------------------------------------------------------------------------------------"""


def changes_detected():
    """
    Check if changes are detected and change the Color of Apply Configuration red.
    Set the global var iChanges to 1 in case someone tries to start without saving
    """
    global iChanges
    core.set_item_color("Apply Configuration", mvGuiCol_Text, (255, 0, 0, 255))
    iChanges = 1
    acScore = core.get_value("Score##match")
    acResult = core.get_value("Result (W/L)##match")
    acMap = core.get_value("Map##match")
    if acScore is False and acResult is True and acMap is True:
        core.set_value("Result (W/L)##match", False)
        core.set_value("Map##match", False)
    if acScore is True and acResult is False and acMap is True:
        core.set_value("Score##match", False)
        core.set_value("Map##match", False)
    if acScore is True and acResult is True and acMap is False:
        core.set_value("Result (W/L)##match", False)
        core.set_value("Score##match", False)

    if acScore is True and acResult is False and acMap is False:
        core.set_value("Result (W/L)##match", True)
        core.set_value("Map##match", True)
    if acScore is False and acResult is True and acMap is False:
        core.set_value("Score##match", True)
        core.set_value("Map##match", True)
    if acScore is False and acResult is True and acMap is True:
        core.set_value("Result (W/L)##match", True)
        core.set_value("Score##match", True)


def disable_all(sender):
    """
    Checkbox Disable all;
    get all checkbox Items and set them to False
    Call the changes_detected function to set iChanges to 1
    """
    items = core.get_all_items()
    for i in items:
        if "stats" in i and "stats" in sender:
            core.set_value(i, False)
        if "match" in i and "match" in sender:
            core.set_value(i, False)
    changes_detected()


def enable_all(sender):
    """
    Checkbox Enable all;
    get all checkbox Items and set them to True ( beside the Disable / Enable all )
    Call the changes_detected function to set iChanges to 1
    """
    items = core.get_all_items()
    for i in items:
        if "stats" in i and "stats" in sender:
            core.set_value(i, True)
            if i == "Disable All##stats":
                core.set_value(i, False)
            if i == "Enable All##stats":
                core.set_value(i, False)
        if "match" in i and "match" in sender:
            core.set_value(i, True)
            if i == "Disable All##match":
                core.set_value(i, False)
            if i == "Enable All##match":
                core.set_value(i, False)
    changes_detected()


""" -------------------------------------------------------------------------------------------------------------------
                                            Animation open Close config
---------------------------------------------------------------------------------------------------------------------"""


def animation_config_color():
    i = 0
    conf = core.get_item_configuration("##Config")
    if conf["width"] < 350:
        core.configure_item("##Config_Colors", show=True)
        core.configure_item("##Help", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * (50))
            i += 0.01
            core.configure_item("##Config", x_pos=0, width=380 + x_pos)
            sleep(0.005)

    else:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * (50))
            i += 0.01
            core.configure_item("##Config", x_pos=0, width=60 - x_pos)
            sleep(0.002)


def animation_config_help():
    i = 0
    conf = core.get_item_configuration("##Config")
    if conf["width"] < 350:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=True)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * (50))
            i += 0.01
            core.configure_item("##Config", x_pos=0, width=380 + x_pos)
            sleep(0.005)

    else:
        core.configure_item("##Config_Colors", show=False)
        core.configure_item("##Help", show=False)
        while i <= 1:
            x_pos = int((1 - math.pow((1 - i), 8)) * (50))
            i += 0.01
            core.configure_item("##Config", x_pos=0, width=60 - x_pos)
            sleep(0.002)


""" -------------------------------------------------------------------------------------------------------------------
                                            OVERLAY START
---------------------------------------------------------------------------------------------------------------------"""


def open_overlay():
    """
    Open the Elo Overlay
    But first check if the FACEIT name is set
    If the FACEIT name isn't correct return
    If changes be made and not saved, return with a warning
    """
    global iChanges
    faceit_name = config_functions.get_faceit_name_from_db()
    if faceit_name:
        if core.does_item_exist("Error##ErrorNoFACEITName"):
            return
        if iChanges == 1:
            set_warning("Configuration not saved, press Apply Configuration")
        else:
            print('layout')
            height = config_functions.check_for_layout()
            hwnd = win32gui.GetForegroundWindow()
            win32gui.MoveWindow(hwnd, 0, 0, 208, height[0] + 39, True)
            simple.hide_item("##Overlay")
            simple.hide_item("##Config")
            win32gui.SetWindowText(hwnd, f"{faceit_name} Elo")
            print('open')
            eloOverlay.show_main()
    else:
        set_error("No FACEIT Name configured")


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


""" -------------------------------------------------------------------------------------------------------------------
                                            BUILD WINDOW WITH DPG
---------------------------------------------------------------------------------------------------------------------"""


def start_build_dpg():

    with simple.window("FACEIT Elo Overlay", on_close=lambda: delete_item("FACEIT Elo Overlay"),
                       no_title_bar=True, no_resize=True):
        """
        Set window configurations
        """
        simple.set_window_pos("FACEIT Elo Overlay", 0, 0)
        core.set_main_window_title("FACEIT Elo Overlay")
        core.set_main_window_size(492, 730)
        core.set_style_frame_rounding(6.00)
        core.add_additional_font("resources/OpenSans-Bold.ttf", size=14.5)

        """
        Initial loads
        """
        db_create.create_database(DBNAME)
        COLOR_List = config_functions.get_color()
        """
        Set some Background and Font Colors
        also the frame rounding and the window size
        """
        core.set_theme_item(mvGuiCol_Text, COLOR_List[1][0], COLOR_List[1][1], COLOR_List[1][2], COLOR_List[1][3])
        core.set_theme_item(mvGuiCol_WindowBg, COLOR_List[3][0], COLOR_List[3][1], COLOR_List[3][2], COLOR_List[3][3])
        core.set_theme_item(mvGuiCol_Border, COLOR_List[4][0], COLOR_List[4][1], COLOR_List[4][2], COLOR_List[4][3])
        core.set_style_frame_border_size(1.00)
        core.set_theme_item(mvGuiCol_Button, COLOR_List[0][0], COLOR_List[0][1], COLOR_List[0][2], COLOR_List[0][3])
        core.set_theme_item(mvGuiCol_ButtonActive, COLOR_List[2][0], COLOR_List[2][1], COLOR_List[2][2],
                            COLOR_List[2][3])
        core.set_theme_item(mvGuiCol_BorderShadow, COLOR_List[0][0], COLOR_List[0][1], COLOR_List[0][2] - 50,
                            COLOR_List[0][3])

    with simple.window('##Overlay', no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=30, y_pos=0,
                       width=445,
                       height=691, no_title_bar=True):
        """
        Set a Header 
        """
        bool_list_faceit, bool_list_match, name = startup()
        core.add_button("Elo Overlay Menu")
        core.set_item_style_var("Elo Overlay Menu", mvGuiStyleVar_FramePadding, [5 * 27, 5 * 3])
        core.add_spacing(count=5)
        """
        Build up the FACEIT Stats configuration 
        """

        with simple.group("##GroupStats"):
            core.add_button("Configure FACEIT Stats##STATS")
            core.set_item_style_var("Configure FACEIT Stats##STATS", mvGuiStyleVar_FramePadding, [5 * 20, 5 * 3])
            core.add_spacing(count=5)

            core.add_input_text("##FaceitName", hint="FACEIT Name Case sensitive", default_value=name,
                                callback=changes_detected)
            core.add_spacing(count=5)
            """
            Faceit Stats header 
            """
            core.add_button("Faceit Stats")
            core.set_item_style_var("Faceit Stats", mvGuiStyleVar_FramePadding, [5 * 26, 5 * 3])
            core.add_spacing(count=2)
            """
            Checkbox group 
            """
            core.add_checkbox("Disable All##stats", default_value=False,
                              callback=lambda sender, data: disable_all(sender))
            core.add_same_line()
            core.add_checkbox("Enable All##stats", default_value=False,
                              callback=lambda sender, data: enable_all(sender))
            core.add_spacing(count=3)
            """
            Checkbox group 
            """
            core.add_checkbox("Current Elo##stats", default_value=bool_list_faceit[0],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("Faceit Rank##stats", default_value=bool_list_faceit[1],
                              callback=changes_detected)
            """
            Checkbox group 
            """
            core.add_checkbox("Elo Gained today##stats", default_value=bool_list_faceit[2],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("Win Streak##stats", default_value=bool_list_faceit[3],
                              callback=changes_detected)

            """
            Checkbox group 
            """
            core.add_checkbox("Total Matches##stats", default_value=bool_list_faceit[4],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("Matches Won##stats", default_value=bool_list_faceit[5],
                              callback=changes_detected)
            core.add_spacing(count=5)
            """
            Last Match header 
            """
            core.add_button("Last Match")
            core.set_item_style_var("Last Match", mvGuiStyleVar_FramePadding, [5 * 26.5, 5 * 3])
            core.add_spacing(count=2)
            """
            Checkbox group 
            """
            core.add_checkbox("Disable All##match", default_value=False,
                              callback=lambda sender, data: disable_all(sender))
            core.add_same_line()
            core.add_checkbox("Enable All##match", default_value=False,
                              callback=lambda sender, data: enable_all(sender))
            core.add_spacing(count=3)
            """
            Checkbox group 
            """
            core.add_checkbox("Score##match", default_value=bool_list_match[0],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("Result (W/L)##match", default_value=bool_list_match[1],
                              callback=changes_detected)
            """
            Checkbox group 
            """
            core.add_checkbox("Map##match", default_value=bool_list_match[2],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("K/D##match", default_value=bool_list_match[3],
                              callback=changes_detected)
            """
            Checkbox group 
            """
            core.add_checkbox("Elo Diff##match", default_value=bool_list_match[4],
                              callback=changes_detected)
            core.add_same_line(xoffset=250)
            core.add_checkbox("Kills##match", default_value=bool_list_match[5],
                              callback=changes_detected)
            """
            Checkbox group 
            """
            core.add_checkbox("Death##match", default_value=bool_list_match[6],
                              callback=changes_detected)
            core.add_spacing(count=5)
            """
            Apply Configuration to the database Button 
            """
            core.add_button("Apply Configuration", callback=save_data)
        """
        Start the Overlay with the current configuration 
        """
        core.add_spacing(count=3)
        core.add_button("Start", callback=open_overlay)
        core.set_item_style_var("Start", mvGuiStyleVar_FramePadding, [5 * 29.5, 5 * 3])

    with simple.window('##Config', no_collapse=True, no_resize=True, no_move=True, no_close=True, x_pos=0, y_pos=1,
                       width=20, height=688, no_title_bar=True):
        core.set_item_color("##Config", mvGuiCol_Text,
                            color=(COLOR_List[1][0], COLOR_List[1][1], COLOR_List[1][2], COLOR_List[1][3]))
        core.set_item_color("##Config", mvGuiCol_WindowBg,
                            color=(COLOR_List[3][0], COLOR_List[3][1], COLOR_List[3][2], COLOR_List[3][3]-10))
        core.set_item_style_var("##Config", mvGuiStyleVar_WindowRounding, value=[6])
        core.set_item_color("##Config", mvGuiCol_Border,
                            color=(COLOR_List[4][0], COLOR_List[4][1], COLOR_List[4][2], COLOR_List[4][3]) )
        core.add_image_button("##ConfigPlus", value="resources/cfg_wheel.png",
                              callback=animation_config_color, frame_padding=1)
        core.add_same_line(xoffset=50)
        with simple.group("##Config_Colors", show=False):
            COLOR_List = config_functions.get_color()
            core.add_text("You can type in the RBG Values or click on the right Color Button")

            core.add_color_edit4(name="Header#Color",
                                 default_value=[COLOR_List[0][0], COLOR_List[0][1], COLOR_List[0][2], COLOR_List[0][3]],
                                 label="Header")
            core.add_color_edit4(name="Text#Color",
                                 default_value=[COLOR_List[1][0], COLOR_List[1][1], COLOR_List[1][2], COLOR_List[1][3]],
                                 label="Text")
            core.add_color_edit4(name="ButtonActive#Color",
                                 default_value=[COLOR_List[2][0], COLOR_List[2][1], COLOR_List[2][2], COLOR_List[2][3]],
                                 label="Button Active")
            core.add_color_edit4(name="BG#Color",
                                 default_value=[COLOR_List[3][0], COLOR_List[3][1], COLOR_List[3][2], COLOR_List[3][3]],
                                 label="Background")
            core.add_color_edit4(name="Outline#Color",
                                 default_value=[COLOR_List[4][0], COLOR_List[4][1], COLOR_List[4][2], COLOR_List[4][3]],
                                 label="Outline")
            core.add_separator()
            core.add_button("Test Colors", callback=test_colors)
            core.add_same_line()
            core.add_button("Reset", callback=reset_colors)
            core.add_button("Save Colors", callback=save_colors)
            core.add_separator()
            core.add_separator()
            scale = config_functions.get_scale()
            core.set_global_font_scale(scale)
            core.add_text("Change The Global Font Size")
            core.add_drag_float("Global Scale", default_value=scale, format="%0.2f", speed=0.01,
                                callback=lambda sender, data: core.set_global_font_scale(
                                    core.get_value("Global Scale")))

            core.add_button("Reset##1", callback=reset_scale)
            core.add_button("Save Size##1", callback=save_scale)
        core.add_spacing(count=5)
        core.add_image_button("##ConfigQuestion", value="resources/q.png",
                              callback=animation_config_help, frame_padding=1)
        core.add_same_line(xoffset=50)
        with simple.group("##Help", show=False):
            core.add_input_text("##HelpIntroText", multiline=True, readonly=True, height=110, width=340,
                                default_value=
                                "Welcome to the help page of the Faceit Overlay\n"
                                "here the options and different possibilities are\n"
                                "explained to you.\n"
                                "Here is a small overview;\n"
                                "1: Start menu\n"
                                "2: Color configuration\n"
                                "3: Overlay"
                                )
            core.add_spacing(count=2)
            core.add_text("1: Start menu")
            core.add_image("##StartmenuImage", value="resources/start_menu.png")
            core.add_input_text("##HelpStartMenuText", multiline=True, height=70, width=340, readonly=True,
                                default_value=
                                "The start menu is the configuration menu\n"
                                "Here you can change colors, global size\n"
                                "Enable / disable stats you want to see\n"
                                "and start the Overlay"
                                )
            core.add_spacing(count=2)
            core.add_text("2: Color configuration")
            core.add_image("##ColorconfImage", value="resources/color_config.png")
            core.add_input_text("##HelpColorConfigText", multiline=True, height=220, width=340, readonly=True,
                                default_value=
                                "Here you can adjust the colors according to your own taste.\n"
                                "The buttons have the following functions:\n\n"
                                "Test Color: Sets the color for the menu so that you can check it.\n"
                                "Reset Color: Sets the colors back to the default value.\n"
                                "Save Color: Saves the colors so that they will be kept\n"
                                "\t\t\t\t\t   on the next startup.\n\n"
                                "To adjust the global size of the texts and heads you can move \n"
                                "the slider to the left or right and then use the buttons \n"
                                "to perform the following functions:\n\n"
                                "Reset: Set the size back to 1.0\n"
                                "Save Size: Save the global size for the next start up"
                                )
            core.add_spacing(count=2)
            core.add_text("3: Overlay")
            core.add_image("##OverlayImage", value="resources/overlay.png")
            core.add_input_text("##HelpOverlayText", multiline=True, height=100, width=340, readonly=True,
                                default_value=
                                "The overlay has basically no functionalities except \n"
                                "that it updates itself regularly (every 60 seconds) \n"
                                "and thus adjusts the values.\n"
                                "But if you click on the headers \n"
                                "FACEIT STATS | LAST GAME  you get back to the start screen.\n"
                                )
    """ ---------------------------------------------------------------------------------------------------------------
                                                START DPG 
        -------------------------------------------------------------------------------------------------------------"""
    core.set_start_callback(eloOverlay.long_process)
    core.enable_docking(dock_space=False)
    core.start_dearpygui(primary_window="FACEIT Elo Overlay")


if __name__ == "__main__":
    __version__ = '0.1'
    __author__ = 'Marco Studer'
    functions.init_logger("overlay")
    start_build_dpg()
