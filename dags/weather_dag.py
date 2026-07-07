from datetime import datetime, timedelta
import os
import sys

# Tells Airflow to look inside the root tree for the pipeline module folder
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from airflow import DAG
from airflow.operators.python import PythonOperator

# Import the core functions
from pipeline.config import LOCATIONS, HOURLY_VARIABLES
from pipeline.extract import extract
from pipeline.load import load_staging, load, load_sqlite3, load_star_schema
from pipeline.transform import transform
from pipeline.validate import validate_weather_data
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# --- WRAPPER FUNCTION FOR TASK 1 ---
def run_ingest_raw_data():
    """Loops through cities, extracts API payload, and dumps directly to disk staging."""
    if not os.path.exists('schema.sql'):
        logger.critical("schema.sql not found. Aborting database operation!")
        raise FileNotFoundError("Required schema file not found.")
    
    for city_name, coords in LOCATIONS.items():
        try:
            data = extract(location=coords, variable=HOURLY_VARIABLES)
            load_staging(data=data, city=city_name)
            logger.info(f"Staged raw payload for {city_name} successfully.")
        except Exception as e:
            logger.error(f"Failed staging raw data for {city_name}: {e}")
            continue

# --- WRAPPER FUNCTION FOR TASK 2 ---
def run_transform_and_load():
    """Wakes up, reads state off disk staging, validates, and builds analytics schemas."""
    import sqlite3
    import json

    db_path = 'data/weather.db'
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Staging database '{db_path}' not found!")
    
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # Query raw data out of staging table (The disk storage hand-off)
    cursor.execute("SELECT city, raw_data FROM staging_weather")
    rows = cursor.fetchall()
    con.close()

    if not rows:
        logger.warning("Staging table is empty. Exiting transformation task early.")
        return

    all_data = []

    # process each staged record
    for city_name, raw_json_str in rows:
        try:
            data = json.loads(raw_json_str)
            data_df = transform(data, city=city_name)

            if validate_weather_data(data_df, city=city_name):
                all_data.append(data_df)
            else:
                logger.error(f"Data validation failed for archived {city_name} run.")
        except Exception as e:
            logger.error(f"Error transforming archived data for {city_name}: {e}")

    if not all_data:
        logger.warning("No clean validated city data frames gathered. Exiting.")
        return 
    
    combined = pd.concat(all_data, ignore_index=True)

    # Final load distribution targets
    load(data=combined)
    load_sqlite3(data=combined)
    load_star_schema(data=combined)
    logger.info("Analytical targets generated successfully.")


# --- DEFINING THE AIRFLOW CONFIGURATION SETTINGS ---
default_args = {
    'owner': 'Oluwabukunmi',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 7, 7),
}

dag = DAG(
    dag_id='nigerian_cities_weather_pipeline',
    default_args=default_args,
    description='Automated production ELT weather pipeline tracking key city metrics',
    schedule_interval='0 0 * * *', # Runs automatically every single day at midnight
    catchup=False
)

# Task definitions using PythonOperators
task_1 = PythonOperator(
    task_id='ingest_raw_data',
    python_callable=run_ingest_raw_data,
    dag=dag
)

task_2 = PythonOperator(
    task_id='transform_and_load',
    python_callable=run_transform_and_load,
    dag=dag
)

# Set dependency, task_2 runs only when task_1 succeeds
task_1 >> task_2