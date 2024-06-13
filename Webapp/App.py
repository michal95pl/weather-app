import datetime
import joblib
import numpy as np
import requests
from flask import Flask, render_template, jsonify
from Database.Database import Database

app = Flask(__name__)

openweather_API_KEY = 'af498f5cac3691870fb684b490ad9408'
city = 'Canberra'


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

    return render_template('index.html', days=days, city=city, mintemp=min_temp, maxtemp=max_temp, raintoday=rain_today)


# rest api
@app.route('/predict', methods=['GET'])
def predict():
    global openweather_API_KEY
    global city

    db = Database()
    if db.check_if_exists_today() is not None:
        print("Date exists in database.")
        date, max_temp, min_temp, rain_today = db.check_if_exists_today()
        return jsonify({
            'Date': date,
            'MinTemp': min_temp,
            'MaxTemp': max_temp,
            'RainToday': rain_today
        })

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
            db.execute_sql_query(f"INSERT INTO weather (Date, Location, MinTemp, MaxTemp, WindGustDir, WindGustSpeed, Humidity, Pressure, RainToday) VALUES "
                                 f"('{datetime.date.today()}', "
                                 f"'{city}', "
                                 f"{min_temp}, "
                                 f"{max_temp}, "
                                 f"{wind_dir}, "
                                 f"{wind_speed}, "
                                 f"{humidity}, "
                                 f"{pressure}, "
                                 f"{prediction[0]})")

        except Exception as e:
            return jsonify({'error': f'Failed to make prediction: {str(e)}'}), 500

        return jsonify({
            'RainToday': prediction[0],
            'MinTemp': min_temp,
            'MaxTemp': max_temp
        })

    else:
        return jsonify({'error': 'Failed to fetch data from OpenWeather API'}), 500


app.run(host='localhost', port=5050)
