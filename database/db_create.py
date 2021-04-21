import logging
import sqlite3


""" -------------------------------------------------------------------------------------------------------------------
                                            CREATE DATABASE
---------------------------------------------------------------------------------------------------------------------"""


def create_database(database_name: str):
    """
    Create Database and Table if it not exist.
    """
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_STATS_FACEIT(
            CurrentElo      TEXT,
            Rank            TEXT,
            EloToday        TEXT,
            WinStreak       TEXT,
            TotalMatches    TEXT,
            MatchesWon      TEXT  
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_STATS_MATCH(
            Map             TEXT,
            Result          TEXT,
            Score           TEXT,
            KD              TEXT,
            EloDiff         TEXT,
            Kills           TEXT,
            Death           TEXT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_COLORS(
            Red            INT,
            Green          INT,
            Blue           INT,
            Trans          INT,
            Type           TEXT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_FACEIT_NAME(
            Name           TEXT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_SCALE(
            Scale           REAL
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_FACEIT_ELO(
            Elo           INT,
            ELODIFF       INT,
            DATE          TEXT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_FACEIT_TARGET_ELO(
            TARGET          TEXT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_REFRESH(
            REFRESH          INT
            )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS CFG_REFRESH_SIGN(
            REFRESH_SIGN          TEXT
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as err:
        logging.error("{}".format(err))
