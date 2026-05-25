import sqlite3

def load(data=None, filename='data/weather_data.csv'):
    data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def load_sqlite3(data=None, db_path='data/weather.db'):
    con = sqlite3.connect(db_path)
    data.to_sql('weather', con, if_exists='replace', index=False)
    con.close() 
    print(f"Data succesfully loaded to {db_path}")

