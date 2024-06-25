import datetime
import threading
import time
import joblib
import numpy as np
import requests
from flask import Flask, render_template, jsonify, request
from Database.Database import Database

app = Flask(__name__)
openweather_API_KEY = 'af498f5cac3691870fb684b490ad9408'
city = 'Canberra'

min_temp_today = None
max_temp_today = None
wind_dir_today = None
wind_speed_today = None
humidity_today = None
pressure_today = None


# main page
@app.route('/')
def index():
    global city

    url = f"http://localhost:5050/predict"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        min_temp = data['MinTemp']
        max_temp = data['MaxTemp']
        rain_today = data['RainToday']

    db = Database()
    today = datetime.date.today() - datetime.timedelta(days=1)
    last_day = today - datetime.timedelta(days=5)

    days = db.get_days_between(last_day, today)

    visitor_ip = request.remote_addr
    is_voted = db.check_if_vote_exists_today(visitor_ip)

    return render_template('index.html', days=days, city=city, mintemp=min_temp, maxtemp=max_temp, raintoday=rain_today,
                           isvoted=is_voted)


# vote pages
@app.route('/vote-yes', methods=['GET'])
def vote_yes():
    db = Database()

    # https://testdriven.io/tips/7e602a4e-edc5-46dd-bcc0-1be2b5a44bb6/
    visitor_ip = request.remote_addr

    today = datetime.date.today().strftime('%Y-%m-%d')

    if db.check_if_vote_exists_today(visitor_ip):
        return render_template('vote-failed.html')
    else:
        db.insert_single_record_vote(today, visitor_ip, 1)

        return render_template('vote-success.html')


@app.route('/vote-no', methods=['GET'])
def vote_no():
    db = Database()
    # https://testdriven.io/tips/7e602a4e-edc5-46dd-bcc0-1be2b5a44bb6/
    visitor_ip = request.remote_addr

    today = datetime.date.today().strftime('%Y-%m-%d')

    if db.check_if_vote_exists_today(visitor_ip):
        return render_template('vote-failed.html')
    else:
        db.insert_single_record_vote(today, visitor_ip, 0)

        return render_template('vote-success.html')


# rest api
@app.route('/predict', methods=['GET'])
def predict():
    global openweather_API_KEY
    global city

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        wind_dir = data['wind']['deg']
        wind_speed = data['wind']['speed']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']

        input_data = np.array([[min_temp, max_temp, wind_dir, wind_speed, humidity, pressure]])

        filename = '../WeatherModel.pkl'
        try:
            model = joblib.load(filename)
        except Exception as e:
            return jsonify({'error': f'Failed to load model: {str(e)}'}), 500

        try:
            prediction = model.predict(input_data)

        except Exception as e:
            return jsonify({'error': f'Failed to make prediction: {str(e)}'}), 500

        return jsonify({
            'RainToday': prediction[0],
            'MinTemp': min_temp,
            'MaxTemp': max_temp
        })

    else:
        return jsonify({'error': 'Failed to fetch data from OpenWeather API'}), 500


# thread functions
def automatic_add():
    db = Database()
    while True:
        if datetime.datetime.now().time().hour == 23 and datetime.datetime.now().time().minute > 55:
            decision = db.decide_if_raining_by_votes()
            today = datetime.date.today()
            if decision:
                if not db.check_if_weather_exists_today():
                    db.insert_single_record_weather(today, city, min_temp_today, max_temp_today, wind_dir_today,
                                                    wind_speed_today, humidity_today, pressure_today, 1)
            else:
                if not db.check_if_weather_exists_today():
                    db.insert_single_record_weather(today, city, min_temp_today, max_temp_today, wind_dir_today,
                                                    wind_speed_today, humidity_today, pressure_today, 0)

            time.sleep(7200)
        time.sleep(30)


def get_midday_weather_values():
    global min_temp_today
    global max_temp_today
    global wind_dir_today
    global wind_speed_today
    global humidity_today
    global pressure_today

    while True:
        if datetime.datetime.now().time().hour == 14 and datetime.datetime.now().time().minute > 30:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                min_temp_today = data['main']['temp_min']
                max_temp_today = data['main']['temp_max']
                wind_dir_today = data['wind']['deg']
                wind_speed_today = data['wind']['speed']
                humidity_today = data['main']['humidity']
                pressure_today = data['main']['pressure']

                time.sleep(7200)
            else:
                print("Failed to fetch data from OpenWeather API")

        time.sleep(30)


# main loop
def start_app():
    print("Starting weather-value thread.. ", end="")
    update_thread1 = threading.Thread(target=get_midday_weather_values)
    update_thread1.start()
    time.sleep(1.5)
    print("DONE")

    print("Starting auto-adding thread.. ", end="")
    update_thread2 = threading.Thread(target=automatic_add)
    update_thread2.start()
    print("DONE")

    print("Starting Flask app..\n")
    app.run(host='localhost', port=5050)


if __name__ == '__main__':
    start_app()
