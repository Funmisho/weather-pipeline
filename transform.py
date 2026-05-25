import pandas as pd
from config import LOCATIONS

def transform(data, city=None):
    data = data['hourly']
    data_df = pd.DataFrame(data)
    data_df['time'] = pd.to_datetime(data_df['time'])

    data_df['city'] = city

    return data_df