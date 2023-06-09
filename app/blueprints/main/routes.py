import datetime
from datetime import datetime
from flask import Request, render_template, g
from flask import Flask, render_template, request
import json
from flask_login import login_required
import requests

from . import bp
from app import app 

app = Flask(__name__)
API_KEY = "311386c7b759f960046806ae93881075"

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)


def convert_to_fahrenheit(celsius):
    return round((celsius * 9/5) + 32, 2)


@bp.route('/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if weather_data:
            temperature = convert_to_fahrenheit(weather_data['main']['temp'])
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            temp_high = convert_to_fahrenheit(weather_data['main']['temp_max'])
            temp_low = convert_to_fahrenheit(weather_data['main']['temp_min'])
            icon_id = weather_data['weather'][0]['icon']
            icon_url = f'http://openweathermap.org/img/w/{icon_id}.png'
            return render_template('index.jinja', temperature=temperature, humidity=humidity,
                                   description=description, temp_high=temp_high, temp_low=temp_low,
                                   icon_url=icon_url, city=city)
        else:
            error_message = 'Location not found! Please try again'
            return render_template('index.jinja', error=error_message)
    return render_template('index.jinja')

