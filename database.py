import sqlite3


TABLE_DAILY_NORM = """CREATE TABLE IF NOT EXISTS DailyWaterNorm(
record_id INTEGER PRIMARY KEY AUTOINCREMENT,
day_id TEXT NOT NULL,
user_id INTEGER NOT NULL,
daily_measure INTEGER NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(user_id)
);"""

TABLE_USERS = """CREATE TABLE IF NOT EXISTS users(
user_id INTEGER NOT NULL UNIQUE,
user_name VARCHAR(50) NOT NULL
);"""

DWN_INSERTION = """INSERT INTO DailyWaterNorm(day_id, user_id, daily_measure) VALUES(?, ?, ?);"""
USER_INSERTION = """INSERT INTO users(user_id, user_name) VALUES(?, ?);"""

CHANGE_MEASURE = """UPDATE DailyWaterNorm SET daily_measure = daily_measure + ? WHERE day_id = ? AND user_id = ?;"""

GET_USER = """SELECT user_id FROM users WHERE user_id = ?;"""
GET_RECORD_BY_CURRENT_DAY = """SELECT daily_measure FROM DailyWaterNorm WHERE day_id = ? AND user_id = ?;"""

GET_STATISTICS_BY_USER = """SELECT daily_measure FROM DailyWaterNorm WHERE user_id = ?;"""


def connection():
    return sqlite3.connect('water.db')


def create_table(connect, query):
    with connect:
        connect.execute(query)


def insert_into_dwn(connect, query, day, user, value):
    with connect:
        connect.execute(query, (day, user, value))


def insert_into_user(connect, query, user_id, user_name):
    with connect:
        connect.execute(query, (user_id, user_name))


def change_measure(connect, query, value, day, user):
    with connect:
        connect.execute(query, (value, day, user))


def get_record_by_current_day(connect, query, day, user):
    with connect:
        return connect.execute(query, (day, user)).fetchone()


def is_user_present_in_db(connect, query, user):
    with connect:
        return connect.execute(query, (user, )).fetchone()


def get_statistics(connect, query, user):
    with connect:
        return connect.execute(query, (user,)).fetchall()
