from config import BASE_URL, LOCATIONS, HOURLY_VARIABLES, FORECAST_DAYS
import requests

def extract(url=BASE_URL, location=None, variable=None, forecast_days=FORECAST_DAYS):
    params={'latitude': location['latitude'], 'longitude': location['longitude'], 'hourly': variable, 'forecast_days':forecast_days}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return data




