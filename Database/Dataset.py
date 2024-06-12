import pandas as pd


class Dataset:
    def __init__(self):
        self.__data = pd.read_csv('weatherAUS.csv')

    def convert_wind_to_degree(self):
        wind_dir = {
            "N": 0,
            "NNE": 22.5,
            "NE": 45,
            "ENE": 67.5,
            "E": 90,
            "ESE": 112.5,
            "SE": 135,
            "SSE": 157.5,
            "S": 180,
            "SSW": 202.5,
            "SW": 225,
            "WSW": 247.5,
            "W": 270,
            "WNW": 292.5,
            "NW": 315,
            "NNW": 337.5,
        }
        self.__data["WindGustDir"] = self.__data["WindGustDir"].map(wind_dir)

    def convert_humidity(self):
        self.__data["Humidity"] = (self.__data["Humidity9am"] + self.__data["Humidity3pm"]) / 2
        self.__data = self.__data.drop(columns=["Humidity9am", "Humidity3pm"])

    def convert_pressure(self):
        self.__data["Pressure"] = (self.__data["Pressure9am"] + self.__data["Pressure3pm"]) / 2
        self.__data = self.__data.drop(columns=["Pressure9am", "Pressure3pm"])

    def drop_unused_columns(self):
        self.__data = self.__data.drop(
            columns=["Rainfall", "Evaporation", "Sunshine", "WindDir9am", "WindDir3pm", "WindSpeed9am", "WindSpeed3pm",
                     "Cloud9am", "Cloud3pm", "Temp9am", "Temp3pm", "RainTomorrow"]
        )

    def convert_rain_today(self):
        self.__data["RainToday"] = self.__data["RainToday"].map({"No": 0, "Yes": 1})

    def get_data(self):
        return self.__data.to_dict(orient='records')
