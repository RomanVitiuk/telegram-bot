import os
from config import ASSISTANT_NAME
import database as db


class UserInterfaceOfGeneralInfo:
    help_info = f'''Hello! My name is {ASSISTANT_NAME} and I am your personal assistant of control daily water norm!\n 
What I`ll do? I will collect information on how much water you drank during the current day and let you know!\n 
To do that fill in and send to me information. Please pay attention that input value must be in integer measure of ml, for example: 250\n
I have several commands which help you to manage me:\n
/help - this is a general information about me and all commands\n
/start - this is a little hint about what you need to do\n
/statistic - show you information about the average value of water drunk per day
'''
    _general_norm = 2000

    @classmethod
    def result(cls, user_id: int, user_name: str, current_day: str) -> str:
        day_for_db = current_day.split()[0]
        was_drank = db.get_record_by_current_day(
            connect=db.connection(),
            query=db.GET_RECORD_BY_CURRENT_DAY,
            day=day_for_db,
            user=int(user_id)
        )[0]
        if was_drank >= cls._general_norm:
            return f'Congratulations {user_name} you done daily water norm!!!'
        left_to_norm = cls._general_norm - was_drank
        return f'''Now {current_day} you was drank {was_drank} ml of water!\n
Don`t give up, to norm left {left_to_norm} ml!!!'''

    @staticmethod
    def start() -> str:
        return '''If you`re new user of this bot or forgot how it work, type help in the input field!\n
Otherwise fill in you value and let`s check how much you drank water this day!'''

    @staticmethod
    def statistics(user_id: int) -> str:
        query_result = db.get_statistics(
            connect=db.connection(),
            query=db.GET_STATISTICS_BY_USER,
            user=user_id
        )
        days = len(query_result)
        stat = round(sum([x[0] for x in query_result]) / days)
        return f'On average you drink {stat} ml of water per a day.'


class InfoHandler:
    def __init__(self, user_id: int, user_name:
                 str, measure_value: str, day: str):
        self._norm = 2000
        self._user_id = user_id
        self._user_name = user_name
        self._measure = int(measure_value)
        self._current_day = day.split()[0]

    def initial_new_user(self):
        db.insert_into_user(connect=db.connection(),
                            query=db.USER_INSERTION,
                            user_id=self._user_id,
                            user_name=self._user_name)

    def add_measure(self):
        db.change_measure(connect=db.connection(),
                          query=db.CHANGE_MEASURE,
                          value=self._measure,
                          day=self._current_day,
                          user=self._user_id)

    def add_new_record(self):
        db.insert_into_dwn(connect=db.connection(),
                           query=db.DWN_INSERTION,
                           day=self._current_day,
                           user=self._user_id,
                           value=0)


def is_first_time_user(user_id: int) -> bool:
    return db.is_user_present_in_db(connect=db.connection(),
                                    query=db.GET_USER,
                                    user=user_id) is None


def is_record_in_db(user_id: int, day: str) -> bool:
    day = day.split()[0]
    return db.get_record_by_current_day(
        connect=db.connection(),
        query=db.GET_RECORD_BY_CURRENT_DAY,
        day=day,
        user=user_id
    ) is None


def initial_db():
    if 'water.db' not in os.listdir(os.getcwd()):
        db.create_table(connect=db.connection(),
                        query=db.TABLE_DAILY_NORM)
        db.create_table(connect=db.connection(),
                        query=db.TABLE_USERS)
