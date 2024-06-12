import sqlite3 as sql

class Database:

    def __init__(self):
        self.connection = sql.connect('../weather.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        querry = """
        CREATE TABLE IF NOT EXISTS weather (
            [Date] TEXT,
            Location TEXT,
            MinTemp REAL,
            MaxTemp REAL,
            WindGustDir REAL,
            WindGustSpeed REAL,
            RainToday TEXT,
            RainTomorrow TEXT,
            Humidity REAL,
            Pressure REAL
        );
        """
        self.cursor.execute(querry)

    # data - dictionary [Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, RainToday, RainTomorrow, Humidity, Pressure]
    def insert_data(self, data):
        for row in data:
            self.cursor.execute(
                "INSERT INTO weather (Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, RainToday, RainTomorrow, Humidity, Pressure) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['Date'], row['Location'], row['MinTemp'], row['MaxTemp'], row['WindGustDir'], row['WindGustSpeed'], row['RainToday'], row['RainTomorrow'], row['Humidity'], row['Pressure'])
            )
        self.connection.commit()

    def __del__(self):
        self.connection.close()
