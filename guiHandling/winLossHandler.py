""" -------------------------------------------------------------------------------------------------------------------
                                            WIN/LOSS HANDLING
---------------------------------------------------------------------------------------------------------------------"""
from dearpygui import core

from config import DBNAME
from database import sqlite3db


def win_los(sender):
    print(sender)
    if sender == "Day##WinLoss" and core.get_value("Day##WinLoss") is False:
        core.set_value("Day##WinLoss", False)
    if sender == "Day##WinLoss" and core.get_value("Day##WinLoss") is True:
        core.set_value("Day##WinLoss", True)
        core.set_value("Week#WinLoss", False)
    if sender == "Week##WinLoss" and core.get_value("Week##WinLoss") is False:
        core.set_value("Week##WinLoss", False)
    if sender == "Week##WinLoss" and core.get_value("Week##WinLoss") is True:
        core.set_value("Day##WinLoss", False)
        core.set_value("Week##WinLoss", True)
    update_win_loss()


def update_win_loss():
    day = core.get_value("Day##WinLoss")
    week = core.get_value("Week##WinLoss")
    data = (day, week)
    print('update')
    print(data)
    sqlite3db.TExecSql(DBNAME, """
                            UPDATE CFG_WIN_LOSS SET Day = ? , Week = ?
                            """, data)
