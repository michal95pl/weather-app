import datetime
import joblib
import numpy as np
import requests
from flask import Flask, render_template, jsonify, request
from Database.Database import Database
from Webapp import WeatherAPI, Updater
import pytz

app = Flask(__name__)
hostname = "localhost"
port = 5000

city = 'Canberra'

gmt10 = pytz.timezone(f'Australia/{city}')


# main page
@app.route('/')
def index():
    global city

    url = f"http://localhost:5000/predict"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rain_today = data['RainToday']
    else:
        return "Predict API error!"

    db = Database()

    today = datetime.datetime.today().astimezone(gmt10).date() - datetime.timedelta(days=1)
    last_day = today - datetime.timedelta(days=5)
    days = db.get_days_between(last_day, today)

    visitor_ip = request.remote_addr
    is_voted = db.check_if_vote_exists_today(visitor_ip)

    temp = WeatherAPI.check_temperature_now()

    return render_template('index.html', days=days, city=city, temp=temp, raintoday=rain_today,
                           isvoted=is_voted, hostname=hostname, port=port)


# vote page
@app.route('/vote', methods=['GET'])
def vote():
    global hostname, port

    decision = request.args.get('decision')

    # https://testdriven.io/tips/7e602a4e-edc5-46dd-bcc0-1be2b5a44bb6/
    visitor_ip = request.remote_addr

    db = Database()

    if db.check_if_vote_exists_today(visitor_ip):
        return render_template('vote.html', isvoted=True, hostname=hostname, port=port)
    else:
        today = datetime.date.today()
        db.insert_single_record_vote(today, visitor_ip, decision)
        return render_template('vote.html', isvoted=False, hostname=hostname, port=port)


# rest api
@app.route('/predict', methods=['GET'])
def predict():
    global city

    min_temp, max_temp, wind_dir, wind_speed, humidity, pressure = WeatherAPI.check_today_weather_values()

    month = datetime.datetime.now().month

    input_data = np.array([[min_temp, max_temp, wind_dir, wind_speed, humidity, pressure, month]])

    filename = '../model.pkl'
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
        'MaxTemp': max_temp,
        'WindDirection': wind_dir,
        'WindSpeed': wind_speed,
        'Humidity': humidity,
        'Pressure': pressure
    })


if __name__ == '__main__':
    Updater.start()
    print("Starting Flask app..\n")
    app.run(host=hostname, port=port)
