import sqlite3
import logging


from functions import functions


def TExecSql(database_name: str, statement: object, bind: object = None) -> object:
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        if bind:
            if bind.__class__.__name__ in ('list', 'tuple'):
                c.execute(statement, bind)
            else:
                c.execute(statement, [bind])
        else:
            c.execute(statement)
        conn.commit()
        conn.close()
    except sqlite3.Error as err:
        logging.error("{}".format(err))


def TExecSqlReadCount(database_name: str, statement: str, bind: list = None):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        if bind:
            if bind.__class__.__name__ in ('list', 'tuple'):
                c.execute(statement, bind)
            else:
                c.execute(statement, [bind])
        else:
            c.execute(statement)
        result = c.fetchone()
        conn.close()
        return functions.ConvertToInt(result)
    except sqlite3.Error as err:
        logging.error("{}".format(err))


def TExecSqlReadMany(database_name: str, statement: str, bind: list = None):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        if bind:
            if bind.__class__.__name__ in ('list', 'tuple'):
                c.execute(statement, bind)
            else:
                c.execute(statement, [bind])
        else:
            c.execute(statement)
        result = c.fetchall()
        conn.close()
        return result
    except sqlite3.Error as err:
        logging.error("{}".format(err))
