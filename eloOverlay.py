import threading
from time import sleep

import win32gui
from dearpygui import core, simple
from dearpygui.core import delete_item
from config import DBNAME
from database import sqlite3db
from functions import config_functions

from faceit import faceit_api
import logging

start_threading = 0

""" -------------------------------------------------------------------------------------------------------------------
                                            THREADING HANDLING
---------------------------------------------------------------------------------------------------------------------"""


class Worker:
    def __init__(self):
        self.iElo = 0
        self.acEloToday = 0
        self.iRank = 0
        self.acResult = ""
        self.acScore = ""
        self.acKd = 0
        self.acMap = ""
        self.iStreak = 0
        self.iMatches = 0
        self.iMatchesWon = 0
        self.acEloDiff = ""
        self.iKills = 0
        self.iDeath = 0

    def run(self):
        """
        Cycle function to update the Overlay every minute
        """
        global start_threading
        while 1:
            try:
                name = sqlite3db.TExecSqlReadMany(DBNAME, """
                                    SELECT name FROM CFG_FACEIT_NAME
                                    """)
                if name:
                    if start_threading == 1:
                        logging.info("Get stats and refresh them")
                        self.iElo, self.acEloToday, self.iRank, \
                        self.acResult, self.acScore, self.acKd, \
                        self.acMap, self.iStreak, self.iMatches, \
                        self.iMatchesWon, self.acEloDiff, self.iKills, \
                        self.iDeath = faceit_api.get_faceit_data_from_api()
                        core.set_value("elotoday##", f"{self.acEloToday}")
                        core.set_value("streak##", f"{self.iStreak}")
                        core.set_value("map##", f"\t{self.acMap}:")
                        core.set_value("result##", f"{self.acResult}")
                        core.set_value("elo##", f"{self.iElo}")
                        core.set_value("rank##", f"{self.iRank}")
                        core.set_value("score##", f"{self.acScore}")
                        core.set_value("matches##", f"{self.iMatches}")
                        core.set_value("matcheswon##", f"{self.iMatchesWon}")
                        core.set_value("elodiffmap##", f"{self.acEloDiff}")
                        core.set_value("kills##", f"{self.iKills}")
                        core.set_value("death##", f"{self.iDeath}")
                        sleep(60)
            except:
                self.run()


def long_process():
    """
    Create Thread and run it !
    """
    w = Worker()
    d = threading.Thread(name='daemon', target=w.run, daemon=True)
    d.start()


""" -------------------------------------------------------------------------------------------------------------------
                                            CHECKBOX HANDLING
---------------------------------------------------------------------------------------------------------------------"""


def add_faceit(iElo, iRank, acEloToday, iStreak, iMatches, iMatchesWon):
    """
    Check all Checkboxes and add the active to the Overlay
    """
    nI = -1
    list_faceit = sqlite3db.TExecSqlReadMany(DBNAME, """
                                            SELECT * FROM CFG_STATS_FACEIT
                                             """
                                             )
    logging.info("Building Faceit stats")
    core.add_button("\t\tFACEIT STATS\t\t", callback=switch_back_to_menu)
    for i in list_faceit[0]:
        nI = nI + 1
        if i == str(1) and nI == 0:
            logging.info("Add Current Elo")
            core.add_text("\tCurrent Elo")
            core.add_same_line(xoffset=130)
            core.add_text("elo##", default_value=f"{iElo}")
        if i == str(1) and nI == 1:
            logging.info("Add Rank")
            core.add_text("\tRank")
            core.add_same_line(xoffset=130)
            core.add_text("rank##", default_value=f"{iRank}")
        if i == str(1) and nI == 2:
            logging.info("Add Elo Today")
            core.add_text("\tElo Today")
            core.add_same_line(xoffset=130)
            core.add_text("elotoday##", default_value=f"{acEloToday}")
        if i == str(1) and nI == 3:
            logging.info("Add Win Streak")
            core.add_text("\tWin Streak")
            core.add_same_line(xoffset=130)
            core.add_text("streak##", default_value=f"{iStreak}")
        if i == str(1) and nI == 4:
            logging.info("Add Tot. Matches")
            core.add_text("\tTot. Matches")
            core.add_same_line(xoffset=130)
            core.add_text("matches##", default_value=f"{iMatches}")
        if i == str(1) and nI == 5:
            logging.info("Add Matches Won")
            core.add_text("\tMatches Won")
            core.add_same_line(xoffset=130)
            core.add_text("matcheswon##", default_value=f"{iMatchesWon}")


def add_last_game(acMap, acResult, acScore, acKd, acEloDiff, iKills, iDeath):
    """
    Check all Checkboxes and add the active to the Overlay
    """
    nI = -1
    list_matches = sqlite3db.TExecSqlReadMany(DBNAME, """
                                            SELECT * FROM CFG_STATS_MATCH
                                             """
                                              )
    core.add_button("\t\t LAST GAME\t\t  ", callback=switch_back_to_menu)
    for i in list_matches[0]:
        nI = nI + 1
        if i == str(1) and nI == 0:
            logging.info("Add Map, result, score")
            core.add_text("map##", default_value=f"\t{acMap}: ")
            core.add_same_line(xoffset=115)
        if i == str(1) and nI == 1:
            core.add_same_line(xoffset=115)
            core.add_text("result##", default_value=f"{acResult}")
        if i == str(1) and nI == 2:
            core.add_same_line(xoffset=130)
            core.add_text("score##", default_value=f"{acScore}")
        if i == str(1) and nI == 3:
            logging.info("Add K/D")
            core.add_text("\tK/D")
            core.add_same_line(xoffset=130)
            core.add_text("kd##", default_value=f"{acKd}")
        if i == str(1) and nI == 4:
            logging.info("Add Elo Diff")
            core.add_text("\tElo Diff")
            core.add_same_line(xoffset=130)
            core.add_text("elodiffmap##", default_value=f"{acEloDiff}")
        if i == str(1) and nI == 5:
            logging.info("Add Kills")
            core.add_text("\tKills:")
            core.add_same_line(xoffset=130)
            core.add_text("kill##", default_value=f"{iKills}")
        if i == str(1) and nI == 6:
            logging.info("Add Deaths")
            core.add_text("\tDeaths:")
            core.add_same_line(xoffset=130)
            core.add_text("death##", default_value=f"{iDeath}")


def switch_back_to_menu():
    logging.info("Switch back to start menu")
    global start_threading
    start_threading = 0
    hwnd = win32gui.GetForegroundWindow()
    win32gui.MoveWindow(hwnd, 0, 0, 492, 730, True)
    simple.show_item("##Overlay")
    simple.show_item("##Config")
    faceit_name = config_functions.get_faceit_name_from_db()
    core.delete_item(f"{faceit_name} Elo")
    win32gui.SetWindowText(hwnd, "FACEIT Elo Overlay")


""" -------------------------------------------------------------------------------------------------------------------
                                            BUILD OVERLAY WINDOW
---------------------------------------------------------------------------------------------------------------------"""


def show_main():
    logging.info("start show_main")
    global start_threading
    heigh, iCountMatch, iCountFaceit = config_functions.check_for_layout()
    name = config_functions.get_faceit_name_from_db()
    with simple.window(f"{name} Elo", height=heigh, width=190,
                       no_title_bar=True, no_resize=True,
                       on_close=lambda: delete_item("FACEIT Elo Overlay"),
                       x_pos=200):
        logging.info("Build the window")
        simple.set_window_pos(f"{name} Elo", 0, 0)
        core.set_main_window_title(f"{name} Elo")
        core.set_main_window_size(width=250, height=heigh)
        # Now the magic happens !
        core.set_style_frame_rounding(6.00)
        """
        Get Data from the API
        """
        logging.info("Get data from the API")
        iElo, acEloToday, iRank, \
        acResult, acScore, acKd, \
        acMap, iStreak, iMatches, \
        iMatchesWon, acEloDiff, iKills, \
        iDeath = faceit_api.get_faceit_data_from_api()
        """
        Build the Faceit Header and Data
        """
        if iCountFaceit > 0:
            logging.info("Build the window for Faceit stats")
            add_faceit(iElo, iRank, acEloToday, iStreak, iMatches, iMatchesWon)
        """
        Build the Last Game Header and Data
        """
        if iCountMatch > 0:
            logging.info("Build the window for Match stats")
            add_last_game(acMap, acResult, acScore, acKd, acEloDiff, iKills, iDeath)

        """
        ! Add some promotion !
        """
        core.add_spacing(count=1)
        core.add_text("powered by Dear PyGui")
        core.add_same_line()
        core.add_image("image##DPG", "resources/6727dpg.ico")

        core.enable_docking(dock_space=False)
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowText(hwnd, f"{name} Elo")
        start_threading = 1
