import datetime
import threading
import time
from Database.Database import Database
from Webapp import WeatherAPI
import pytz

min_temp_today = None
max_temp_today = None
wind_dir_today = None
wind_speed_today = None
humidity_today = None
pressure_today = None

city = "Canberra"

gmt10 = pytz.timezone(f'Australia/{city}')

automatic_add_flag = True
get_midday_weather_values_flag = True

# thread functions
def automatic_add(db: Database):
    global min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today
    global automatic_add_flag

    if datetime.datetime.now().astimezone(gmt10).time().hour == 23 and datetime.datetime.now().astimezone(gmt10).time().minute > 55 and automatic_add_flag:
        decision = db.decide_if_raining_by_votes()

        today = datetime.datetime.today()
        today = today.astimezone(gmt10).date()

        if not db.check_if_weather_exists_today():
            decision_value = 1 if decision else 0
            db.insert_single_record_weather(today, city, min_temp_today, max_temp_today, wind_dir_today,
                                            wind_speed_today, humidity_today, pressure_today, decision_value)
            print("THREAD 1: Weather record was added.")

            # wait for the next day
            automatic_add_flag = False

    else:
        automatic_add_flag = True


def get_midday_weather_values():
    global min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today
    global get_midday_weather_values_flag

    if (((datetime.datetime.now().astimezone(gmt10).time().hour == 14 and datetime.datetime.now().astimezone(gmt10).time().minute > 30)
            or min_temp_today is None or max_temp_today is None or wind_dir_today is None or wind_speed_today is None)
            and get_midday_weather_values_flag):
        min_temp_today, max_temp_today, wind_dir_today, wind_speed_today, humidity_today, pressure_today = WeatherAPI.check_today_weather_values()
        print("THREAD 1: Weather values are assigned.")

        # wait for the next day
        get_midday_weather_values_flag = False

    else:
        get_midday_weather_values_flag = True


def background_thread():

    print("Thread started\n")

    db = Database()

    while True:
        automatic_add(db)
        get_midday_weather_values()
        time.sleep(60)


def start():
    threading.Thread(target=background_thread).start()


# launch updater standalone
if __name__ == '__main__':
    start()
