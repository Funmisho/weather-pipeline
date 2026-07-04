import sqlite3
import logging
from config import LOCATIONS
import json

# setting up logging for this file
logger = logging.getLogger(__name__)

def load(data=None, filename='data/weather_data.csv'):
    data.to_csv(filename, index=False)
    logger.info(f"Data successfuly saved to {filename}")

def load_sqlite3(data=None, db_path='data/weather.db'):
    con = sqlite3.connect(db_path)
    data.to_sql('weather', con, if_exists='replace', index=False)
    con.close() 
    logger.info(f"Data succesfully loaded to {db_path}")

def load_star_schema(data=None, db_path='data/weather.db'):
    logger.info(f"Connecting to database to load star schema: {db_path}")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # create tables from schema file
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    records_inserted = 0
    
    # looping through the transformed dataframe
    for _, row in data.iterrows():
        city = row['city']
        timestamp = row['time'] # this is a pandas datetime object


        # insert into dim_location
        cursor.execute(
           "INSERT OR IGNORE INTO dim_location (city, latitude, longitude) VALUES(?, ?, ?)",
           (city, LOCATIONS[city]['latitude'], LOCATIONS[city]['longitude'])
        )
        
        # fetch ID
        cursor.execute(
            "SELECT location_id FROM dim_location WHERE city = ?",
            (city,)
        )
        location_id = cursor.fetchone()[0]

        # insert into dim_time
        cursor.execute(
            "INSERT OR IGNORE INTO dim_time (timestamp, date, hour, day_of_week, month, year) VALUES(?, ?, ?, ?, ?, ?)",
            (str(timestamp), str(timestamp.date()), int(timestamp.hour), timestamp.day_name(), int(timestamp.month), int(timestamp.year))
        )

        # fetch time_id
        cursor.execute(
            "SELECT time_id FROM dim_time WHERE timestamp = ?",
            (str(timestamp),)
        )
        time_id = cursor.fetchone()[0]

        # insert into fact_weather
        cursor.execute(
            "INSERT OR IGNORE INTO fact_weather (location_id, time_id, temperature_2m, precipitation, windspeed_10m) VALUES(?, ?, ?, ?, ?)",
            (location_id, time_id, row['temperature_2m'], row['precipitation'], row['windspeed_10m'])
        )
        records_inserted += 1

    con.commit()
    con.close()
    logger.info(f"Star schema processing complete. Iterated through {records_inserted} rows.")

def load_staging(data=None, city=None, db_path='data/weather.db'):
    logger.info(f"Staging raw JSON data for {city} into database...")
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # create staging table from schema script
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    # turn raw API dictionary into a text string
    json_string = json.dumps(data)

    # insert into staging table
    cursor.execute(
        "INSERT INTO staging_weather (city, raw_data) VALUES (?, ?)",
        (city, json_string)
    )

    con.commit()
    con.close()
    logger.info(f"Successfully staged {city}.")


