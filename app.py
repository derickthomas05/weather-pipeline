import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

@st.cache_data
def load_data():
    with sqlite3.connect("weather.db") as conn:
        return pd.read_sql("SELECT * FROM weather_hourly ORDER BY timestamp",
                           conn, parse_dates=["timestamp"])

df = load_data()
st.title("Troy, NY Weather Dashboard")

days = st.slider("Days to show", 1, 8, 7)
view = df[df["timestamp"] >= df["timestamp"].max() - pd.Timedelta(days=days)]

c1, c2, c3 = st.columns(3)
c1.metric("Avg temp (°F)", f"{view['temp_f'].mean():.1f}")
c2.metric("Max temp (°F)", f"{view['temp_f'].max():.1f}")
c3.metric("Avg wind (mph)", f"{view['wind_mph'].mean():.1f}")

st.plotly_chart(px.line(view, x="timestamp", y="temp_f", title="Temperature (°F)"))
st.plotly_chart(px.line(view, x="timestamp", y="humidity_pct", title="Humidity (%)"))

daily = (view.assign(date=view["timestamp"].dt.date)
         .groupby("date")["temp_f"].agg(["min", "max", "mean"]).round(1).reset_index())
st.subheader("Daily summary")
st.dataframe(daily)