import pandas as pd
import sqlite3 as sql


class Dataset:
    def __init__(self):
        self.__conn = sql.connect("../weather.db")
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        self.__conn.close()

    def get_data(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM weather", self.__conn)
        return df
