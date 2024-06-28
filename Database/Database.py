import sqlite3 as sql
import datetime


class weather_record:
    def __init__(self, date, rain_today):
        self.date = date
        self.rain_today = rain_today


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
            Humidity REAL,
            Pressure REAL,
            RainToday REAL
        );
        """
        self.cursor.execute(querry)

        querry = """
                CREATE TABLE IF NOT EXISTS vote (
                    [date] TEXT,
                    ip TEXT,
                    decision INTEGER
                );
                """
        self.cursor.execute(querry)

    # data - dictionary [Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, RainToday, RainTomorrow, Humidity, Pressure]
    def insert_data(self, data):
        for row in data:
            self.cursor.execute(
                "INSERT INTO weather (Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, Humidity, Pressure, RainToday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (row['Date'], row['Location'], row['MinTemp'], row['MaxTemp'], row['WindGustDir'], row['WindGustSpeed'],
                 row['Humidity'], row['Pressure'], row['RainToday'])
            )
        self.connection.commit()

    def insert_single_record_weather(self, date, location, mintemp, maxtemp, windgustdir, windgustspeed, humidity, pressure, raintoday):
        self.cursor.execute(
            "INSERT INTO weather (Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, Humidity, Pressure, RainToday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (date, location, mintemp, maxtemp, windgustdir, windgustspeed, humidity, pressure, raintoday)
        )
        self.connection.commit()

    def insert_single_record_vote(self, date, ip, decision):
        self.cursor.execute(
            "INSERT INTO vote (date, ip, decision) VALUES (?, ?, ?)",
            (date, ip, decision)
        )
        self.connection.commit()

    def get_days_between(self, start, end):
        self.cursor.execute("SELECT [DATE], RainToday "
                            "FROM weather WHERE Date BETWEEN ? AND ? "
                            "ORDER BY Date DESC LIMIT 5", (start, end))
        rows = self.cursor.fetchall()
        days = []
        for row in rows:
            day = weather_record(row[0], row[1])
            days.append(day)
        return days

    def check_if_weather_exists_today(self):
        today = datetime.date.today()
        self.cursor.execute("SELECT * FROM weather WHERE Date = ?", (today,))
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return False
        else:
            return True

    def check_if_vote_exists_today(self, ip):
        today = datetime.date.today()
        self.cursor.execute("SELECT * FROM vote WHERE Date = ? AND ip = ?", (today, ip))
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            return False
        else:
            return True

    def decide_if_raining_by_votes(self):
        today = datetime.date.today()
        self.cursor.execute("SELECT * FROM vote WHERE date = ? AND decision = 1", (today,))
        yes = self.cursor.fetchall()

        self.cursor.execute("SELECT * FROM vote WHERE date = ? AND decision = 0", (today,))
        no = self.cursor.fetchall()

        if len(yes) > len(no):
            return True
        else:
            return False

    def execute_sql_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def __del__(self):
        self.connection.close()
