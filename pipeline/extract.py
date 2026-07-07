from pipeline.config import BASE_URL, LOCATIONS, HOURLY_VARIABLES, FORECAST_DAYS
import requests
import logging

# setting up logging for this file
logger = logging.getLogger(__name__)

def extract(url=BASE_URL, location=None, variable=None, forecast_days=FORECAST_DAYS):
    params = {
        'latitude': location['latitude'],
        'longitude': location['longitude'],
        'hourly': variable,
        'forecast_days':forecast_days
    }

    try:
        # debug log to see what script is doing
        logger.debug(f"Requesting data for coordinates: {location['latitude']}, {location['longitude']}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API Extraction request failed for coordinates ({location['latitude']}, {location['longitude']}): {e}")
        raise # reraise the error so pipeline.py's try-except loop can handle skipping this city safely




