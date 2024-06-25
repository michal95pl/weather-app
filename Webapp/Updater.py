import datetime
import threading
import time
from Database.Database import Database
from Webapp import WeatherAPI

min_temp_today = None
max_temp_today = None
wind_dir_today = None
wind_speed_today = None
humidity_today = None
pressure_today = None

city = "Canberra"


# thread functions
def automatic_add():
    global min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today

    db = Database()
    while True:
        if datetime.datetime.now().time().hour == 23 and datetime.datetime.now().time().minute > 55:
            decision = db.decide_if_raining_by_votes()
            today = datetime.date.today()

            if not db.check_if_weather_exists_today():
                decision_value = 1 if decision else 0
                db.insert_single_record_weather(today, city, min_temp_today, max_temp_today, wind_dir_today,
                                                wind_speed_today, humidity_today, pressure_today, decision_value)
                print("THREAD 2: Weather record was added.")

            time.sleep(7200)
        time.sleep(30)


def get_midday_weather_values():
    global min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today

    while True:
        if ((datetime.datetime.now().time().hour == 14 and datetime.datetime.now().time().minute > 30)
                or min_temp_today is None or max_temp_today is None or wind_dir_today is None or wind_speed_today is None):
            min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today = WeatherAPI.check_today_weather_values()
            print("THREAD 1: Weather values are assigned.")
            time.sleep(7200)
        time.sleep(30)


# start background threads
def start_background_threads():
    print("Starting weather-value thread.. ")
    update_thread1 = threading.Thread(target=get_midday_weather_values)
    update_thread1.start()
    time.sleep(2.5)

    print("Starting auto-adding thread.. ")
    update_thread2 = threading.Thread(target=automatic_add)
    update_thread2.start()


# launch updater standalone
if __name__ == '__main__':
    start_background_threads()
