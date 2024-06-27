import pandas as pd
import sqlite3 as sql


class Dataset:
    def __init__(self):
        self.__conn = sql.connect("../weather.db")
        self.__cursor = self.__conn.cursor()
        self.__data = pd.read_sql_query("SELECT * FROM weather", self.__conn)
        self.__data = self.__data.dropna()

        self.__data["Month"] = self.__data["Date"].apply(lambda x: int(x[5:7]))

    def __del__(self):
        self.__conn.close()

    def show_correlation(self):
        print("Correlation RainToday:")
        corr_data = self.__data.drop(["Date", "Location"], axis=1)
        corr_matrix = corr_data.corr()
        print(corr_matrix["RainToday"].sort_values(ascending=False))
        print()

    def get_locations(self):
        return self.__data["Location"].unique()

    def get_data_by_location(self, location: str) -> pd.DataFrame:
        data = self.__data[self.__data["Location"] == location]
        return data
