-- Table 1: dim_location
CREATE TABLE IF NOT EXISTS dim_location (
	location_id INTEGER PRIMARY KEY AUTOINCREMENT,
	city TEXT NOT NULL UNIQUE,
	latitude REAL,
	longitude REAL
);

-- Table 2: dim_time
CREATE TABLE IF NOT EXISTS dim_time (
	time_id INTEGER PRIMARY KEY AUTOINCREMENT,
	timestamp TEXT NOT NULL UNIQUE,
	date TEXT NOT NULL,
	hour INTEGER NOT NULL,
	day_of_week TEXT NOT NULL,
	month INTEGER NOT NULL,
	year INTEGER NOT NULL
);

-- Table 3: fact_weather
CREATE TABLE IF NOT EXISTS fact_weather (
	weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
	location_id INTEGER, 
	time_id INTEGER,
	temperature_2m REAL,
	precipitation REAL,
	windspeed_10m REAL,
	FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
	FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
	UNIQUE(location_id, time_id)
);

-- Table 4: staging_weather
CREATE TABLE IF NOT EXISTS staging_weather (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	city TEXT NOT NULL,
	raw_data TEXT NOT NULL,
	extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)