import datetime
import requests
from flask import Flask, render_template
from Database.Database import Database

app = Flask(__name__)

openweather_API_KEY = 'af498f5cac3691870fb684b490ad9408'

# main page
@app.route('/')
def index():
    global openweather_API_KEY

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Canberra&appid={openweather_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        min_temp = data['main']['temp_min']
        max_temp = data['main']['temp_max']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        wind_dir = data['wind']['deg']

    today = datetime.date.today()
    last_day = today - datetime.timedelta(days=5)

    db = Database()

    return render_template('index.html')

# rest api
@app.route('/predict')
def predict():
    return "1";

app.run(host='localhost', port=5050)