import sqlite3
import requests
import pandas as pd

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": 42.73, "longitude": -73.69,   # Troy, NY
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "temperature_unit": "fahrenheit", "wind_speed_unit": "mph",
    "past_days": 7, "forecast_days": 1, "timezone": "America/New_York",
}

def extract():
    r = requests.get(URL, params=PARAMS, timeout=30)
    r.raise_for_status()
    return r.json()

def transform(raw):
    df = pd.DataFrame(raw["hourly"]).rename(columns={
        "time": "timestamp", "temperature_2m": "temp_f",
        "relative_humidity_2m": "humidity_pct", "wind_speed_10m": "wind_mph"})
    df = df.dropna()
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    return df

def load(df, db="weather.db"):
    with sqlite3.connect(db) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS weather_hourly (
            timestamp TEXT PRIMARY KEY, temp_f REAL,
            humidity_pct REAL, wind_mph REAL)""")
        conn.executemany(
            "INSERT OR REPLACE INTO weather_hourly VALUES (?,?,?,?)",
            df[["timestamp", "temp_f", "humidity_pct", "wind_mph"]]
            .itertuples(index=False, name=None))
    print(f"Loaded {len(df)} rows into {db}")

if __name__ == "__main__":
    load(transform(extract()))