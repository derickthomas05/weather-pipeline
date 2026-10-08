# Weather Pipeline and Dashboard

Python ETL pipeline that pulls hourly weather data from the Open-Meteo API,
cleans it with pandas, stores it in SQLite, and displays it in a Streamlit dashboard.

## Architecture
API -> pandas -> SQLite -> Streamlit

## Setup
pip install -r requirements.txt
python pipeline.py
streamlit run app.py

## Screenshot
![Dashboard] (screenshot.png) (screenshot1.png)


## What I learned
- How to build a simple ETL pipeline: extracting JSON from a REST API with Python, cleaning it with pandas, and loading it into a SQLite database.
- Why a primary key matters. Using the timestamp as the key lets the pipeline run repeatedly without creating duplicate rows.
- How to turn a database into an interactive Streamlit dashboard with filters, metrics, and charts.sentences