# Weather Data Pipeline

A Python ETL pipeline that pulls 3-day hourly weather forecasts for 
three Nigerian cities from the Open-Meteo API, transforms the data 
into a structured format, and stores it locally as both CSV and SQLite.

## What it does

- Fetches hourly temperature, precipitation, and wind speed data for
  Lagos, Abuja, and Kano from the Open-Meteo public REST API
- Parses and flattens nested JSON responses into a pandas DataFrame
- Converts timestamps to datetime objects and tags each row with its city
- Loads the cleaned data to both a CSV file and a SQLite database
- Handles API failures per city gracefully without crashing the pipeline

## Tech stack

- Python 3
- pandas
- requests
- sqlite3 (built-in)

## How to run it

1. Clone the repository
   git clone https://github.com/Funmisho/weather-pipeline.git
   cd weather-pipeline

2. Create and activate a virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the pipeline
   python3 pipeline.py

## Project structure

```
weather-pipeline/
├── config.py       # API base URL, city coordinates, and parameters
├── extract.py      # Fetches raw JSON data from the Open-Meteo API
├── transform.py    # Parses JSON, builds DataFrame, formats timestamps
├── load.py         # Saves data to CSV and SQLite
├── pipeline.py     # Orchestrates the full ETT pipeline
├── requirements.txt
└── data/           # Output folder (generated on run, gitignored)
```

## Sample output

| time                | temperature_2m | precipitation | windspeed_10m | city  |
|---------------------|----------------|---------------|---------------|-------|
| 2026-05-25 00:00:00 | 27.5           | 0.4           | 3.0           | lagos |
| 2026-05-25 01:00:00 | 26.9           | 0.0           | 1.8           | lagos |
| 2026-05-25 02:00:00 | 26.5           | 0.5           | 5.4           | lagos |
| 2026-05-25 03:00:00 | 25.1           | 0.5           | 2.7           | lagos |
| 2026-05-25 04:00:00 | 24.6           | 2.6           | 5.3           | lagos |