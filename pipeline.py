from extract import extract
from transform import transform 
from config import BASE_URL, LOCATIONS, HOURLY_VARIABLES, FORECAST_DAYS
import requests
import pandas as pd
from load import load, load_sqlite3, load_star_schema, load_staging
from validate import validate_weather_data
import logging

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'), # saves to file
        logging.StreamHandler() # prints to terminal
    ]
)

# setting up logging for this file
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Starting weather data pipeline...")
    all_data = []

    for city_name, coords in LOCATIONS.items():
        try:
            data = extract(location=coords, variable=HOURLY_VARIABLES)

            load_staging(data=data, city=city_name)
            data_df = transform(data, city=city_name)

            if validate_weather_data(data_df, city=city_name):
                all_data.append(data_df)
                logger.info(f"Successfully processed {city_name}")
            else:
                logger.error(f"Skipping {city_name} - failed validation")


        except Exception as e:
            logger.exception(f"failed to process {city_name}: {e}")
            continue

    if not all_data:
        logger.warning("No data was collected. Exiting pipeline early.")
        return
    
    combined = pd.concat(all_data, ignore_index=True)

    logger.info(f"Combining data completed. Total records: {len(combined)}")
    load(data=combined)
    load_sqlite3(data=combined)
    load_star_schema(data=combined)

    logger.info("Pipeline executed successfully finished.")

if __name__ == "__main__":
    run_pipeline()