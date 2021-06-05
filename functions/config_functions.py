import glob
from config import DBNAME
from database import sqlite3db
from functions import functions
from datetime import date
import logging

""" -------------------------------------------------------------------------------------------------------------------
                                                CHECK HANDLING
---------------------------------------------------------------------------------------------------------------------"""


def check_if_dbfile_exists():
    logging.info("start check_if_dbfile_exists")
    """
    Check if a db-file exists in the current directory.
    return : 1 if exists
             0 if not exists
    """
    for file in glob.glob("*.sqlite"):
        if file:
            logging.info("found a database file")
            return 1
    return 0


def check_if_elo_entry_exists():
    """
    Check if there is any entry in CFG_STATS_FACEIT.
    return : 1 if exists
             0 if not exists
    """
    logging.info("start check_if_elo_entry_exists")
    today = date.today()
    iRv = sqlite3db.TExecSqlReadCount(DBNAME, """
            SELECT COUNT(*) FROM CFG_FACEIT_ELO
            WHERE DATE = ?
            """, str(today))
    if iRv > 0:
        return 1
    else:
        return 0


def check_if_config_entry_exists(statement):
    """
    Check if there is any entry in CFG_STATS_FACEIT.
    return : 1 if exists
             0 if not exists
    """
    logging.info("start check_if_config_entry_exists")
    iRv = sqlite3db.TExecSqlReadCount(DBNAME, statement)
    if iRv > 0:
        return 1
    else:
        return 0


def get_win_loss():
    """
    Get the refresh time from the DB.
    return : int from DB
    """
    logging.info("start get_win_loss")
    iRv = check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_WIN_LOSS
            """)
    if iRv > 0:
        win_loss = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM CFG_WIN_LOSS
                                """)
        return win_loss
    return False, False


def get_refresh_sign():
    """
    Get the refresh sign from the DB.
    return : int from DB
    """
    logging.info("start get_refresh_sign")
    iRv = check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_REFRESH
            """)
    if iRv > 0:
        refresh = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM CFG_REFRESH_SIGN
                                """)
        return functions.listToStringWithoutBracketsAndAT(refresh)
    else:
        refresh = True
    return refresh


def get_refresh():
    """
    Get the refresh time from the DB.
    return : int from DB
    """
    logging.info("start get_refresh")
    iRv = check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_REFRESH
            """)
    if iRv > 0:
        refresh = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM CFG_REFRESH
                                """)
        return functions.ConvertToInt(refresh[0])
    else:
        refresh = 60
    return refresh


def get_scale():
    """
    Get the scale from the DB.
    return : Float from DB
             Default Float 1.00
    """
    logging.info("start get_scale")
    iRv = check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_SCALE
            """)
    if iRv > 0:
        scale = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM CFG_SCALE
                                """)
        scale = functions.ConvertToFloat(scale[0])
        return scale
    else:
        scale = 1.00
    return scale


def get_color():
    """
    Get the colors from the DB.
    If no color entry exists return the default values
    return : List with saved colors
             List with default colors
    """
    logging.info("start get_color")
    iRv = check_if_config_entry_exists("""
            SELECT COUNT(*) FROM CFG_COLORS
            """)
    if iRv > 0:
        colors = sqlite3db.TExecSqlReadMany(DBNAME, """
                                SELECT * FROM CFG_COLORS
                                """)
    else:
        colors = (66, 150, 250, 255, 'Header'), \
                 (255, 255, 255, 255, 'Text'), \
                 (15, 135, 250, 255, 'ButtonActive'), \
                 (15, 15, 15, 255, 'Background'), \
                 (255, 255, 255, 255, 'Outline')
    return colors


def get_faceit_name_from_db():
    """
    Get faceit name from database and return the name
    """
    logging.info("start get_faceit_name_from_db")
    name = sqlite3db.TExecSqlReadMany(DBNAME, """
                        SELECT name FROM CFG_FACEIT_NAME
                        """)
    if name:
        name = functions.listToStringWithoutBracketsAndAT(name[0])
    return name


def get_elo_goal_from_db():
    """
    Get the Elo Goal from database and return the Value
    """
    logging.info("start get_elo_goal_from_db")
    acEloGoal = sqlite3db.TExecSqlReadMany(DBNAME, """
                        SELECT TARGET FROM CFG_FACEIT_TARGET_ELO
                        """)
    if acEloGoal:
        acEloGoal = functions.listToStringWithoutBracketsAndAT(acEloGoal[0])
    else:
        return ""
    return acEloGoal


def check_for_layout():
    """
    Check which Checkboxes are active and set the height of the overlay
    """
    logging.info("start check_for_layout")
    iCountFaceit = 0
    iCountMatch = 0
    heigh = 0
    list_faceit = sqlite3db.TExecSqlReadMany(DBNAME, """
                                            SELECT * FROM CFG_STATS_FACEIT
                                             """
                                             )
    list_matches = sqlite3db.TExecSqlReadMany(DBNAME, """
                                            SELECT * FROM CFG_STATS_MATCH
                                             """
                                              )
    acEloGoal = sqlite3db.TExecSqlReadCount(DBNAME, """
                                            SELECT COUNT(*) FROM CFG_FACEIT_TARGET_ELO""")
    WinLoss = get_win_loss()
    if WinLoss[0][0] == "1":
        iCountFaceit = iCountFaceit + 1
    if WinLoss[0][1] == "1":
        iCountFaceit = iCountFaceit + 1
    for i in list_faceit[0]:
        if i == str(1):
            iCountFaceit = iCountFaceit + 1
    if acEloGoal:
        iCountFaceit = iCountFaceit + 1
    nI = 0
    for i in list_matches[0]:
        if i == str(1):
            if nI > 1:
                iCountMatch = iCountMatch + 1
        nI = nI + 1
    iCount = iCountFaceit + iCountMatch
    print(iCount)
    if iCount == 14:
        heigh = 345
    if iCount == 13:
        heigh = 330
    if iCount == 12:
        heigh = 305
    if iCount == 11:
        heigh = 285
    if iCount == 10:
        heigh = 265
    if iCount == 9:
        heigh = 250
    if iCount == 8:
        heigh = 230
    if iCount == 7:
        heigh = 210
    if iCount == 6:
        heigh = 195
    if iCount == 5:
        heigh = 170
    if iCount == 4:
        heigh = 155
    if iCount == 3:
        heigh = 150
    if iCount == 2:
        heigh = 130
    if iCount == 1:
        heigh = 120
    return heigh, iCountMatch, iCountFaceit
