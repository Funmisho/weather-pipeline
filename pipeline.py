from extract import extract
from transform import transform 
from config import BASE_URL, LOCATIONS, HOURLY_VARIABLES, FORECAST_DAYS
import requests
import pandas as pd
from load import load
from load import load_sqlite3

def run_pipeline():
    all_data = []
    for city_name, coords in LOCATIONS.items():
        try:
            data = extract(location=coords, variable=HOURLY_VARIABLES)
            data_df = transform(data, city=city_name)
            all_data.append(data_df)
            print(f"Successfully processed {city_name}")
        except Exception as e:
            print(f"failed to process {city_name}: {e}")
            continue

    if not all_data:
        print("No data was collected. Exiting.")
        return
    combined = pd.concat(all_data, ignore_index=True)
    load(data=combined)

    load_sqlite3(data=combined)

if __name__ == "__main__":
    run_pipeline()