import pandas as pd
from config import LOCATIONS
import logging

# setting up logging for this file
logger = logging.getLogger(__name__)

def transform(data, city=None):
    logger.debug(f"Transforming raw JSON data into dataframe for city: {city}")

    data = data['hourly']
    data_df = pd.DataFrame(data)
    data_df['time'] = pd.to_datetime(data_df['time'])

    data_df['city'] = city

    return data_df