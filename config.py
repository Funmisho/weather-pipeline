BASE_URL = "https://api.open-meteo.com/v1/forecast"

LOCATIONS = {
    "lagos": {"latitude": 6.5244, "longitude": 3.3792},
    "abuja": {"latitude": 9.0765, "longitude": 7.3986},
    "kano":  {"latitude": 12.0022, "longitude": 8.5920},
}

HOURLY_VARIABLES = ["temperature_2m", "precipitation", "windspeed_10m"]

FORECAST_DAYS = 3