import datetime
import joblib
import numpy as np
import requests
from flask import Flask, render_template, jsonify, request
from Database.Database import Database
from Webapp import WeatherAPI, Updater

app = Flask(__name__)
hostname = "localhost"
port = 5000

city = 'Canberra'


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
    today = datetime.date.today() - datetime.timedelta(days=1)
    last_day = today - datetime.timedelta(days=5)

    days = db.get_days_between(last_day, today)

    visitor_ip = request.remote_addr
    is_voted = db.check_if_vote_exists_today(visitor_ip)
    temp = WeatherAPI.check_temperature_now()

    return render_template('index.html', days=days, city=city, temp=temp, raintoday=rain_today,
                           isvoted=is_voted, hostname=hostname, port=port)


# vote pages
@app.route('/vote-yes', methods=['GET'])
def vote_yes():
    db = Database()

    # https://testdriven.io/tips/7e602a4e-edc5-46dd-bcc0-1be2b5a44bb6/
    visitor_ip = request.remote_addr

    today = datetime.date.today()

    if db.check_if_vote_exists_today(visitor_ip):
        return render_template('vote.html', isvoted=True)
    else:
        db.insert_single_record_vote(today, visitor_ip, 1)
        return render_template('vote.html', isvoted=False)


@app.route('/vote-no', methods=['GET'])
def vote_no():
    db = Database()

    # https://testdriven.io/tips/7e602a4e-edc5-46dd-bcc0-1be2b5a44bb6/
    visitor_ip = request.remote_addr

    today = datetime.date.today()

    if db.check_if_vote_exists_today(visitor_ip):
        return render_template('vote.html', isvoted=True)
    else:
        db.insert_single_record_vote(today, visitor_ip, 0)
        return render_template('vote.html', isvoted=False)


# rest api
@app.route('/predict', methods=['GET'])
def predict():
    global city

    min_temp, max_temp, wind_dir, wind_speed, humidity, pressure = WeatherAPI.check_today_weather_values()

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
        'MaxTemp': max_temp,
        'WindDirection': wind_dir,
        'WindSpeed': wind_speed,
        'Humidity': humidity,
        'Pressure': pressure
    })


if __name__ == '__main__':
    Updater.start_background_threads()
    print("Starting Flask app..\n")
    app.run(host=hostname, port=port)
