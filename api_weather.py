import requests
import config_bd
from bot_command import weather_in_api
def get_weather(api_key, location, date, lang):
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&dt={date}&lang={lang}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current_temp = data['forecast']['forecastday'][0]['day']['avgtemp_c']
        weather_condition = data['forecast']['forecastday'][0]['day']['condition']['text']
        wind_speed = data['forecast']['forecastday'][0]['day']['maxwind_kph']
        weather_in_api(current_temp, weather_condition, wind_speed)
    else:
        print('Ошибка при получении данных о погоде')

def check_weather(location, date):
    api_key = config_bd.get_token('WT_TOKEN')
    lang = 'ru'
    get_weather(api_key, location, date, lang)