"""
Functions to visualise data on streamlit.
"""
import altair as alt
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
import streamlit as st

from database import get_database_connection, load_all_plant_data
from utilities import get_latest_data


def get_latest_temperature_readings(plants: DataFrame, sort_ascending):
    """
    Returns an altair bar chart that shows the latest temperature readings for each plant.
    """
    latest_data = get_latest_data(plants)

    latest_data["Plant Name"] = latest_data[["plant_name"]]
    latest_data["Temperature (°C)"] = latest_data[["temperature"]]

    latest_data = latest_data[["Plant Name", "Temperature (°C)"]]

    sort_order = "x" if sort_ascending else "-x"

    latest_temp_readings = alt.Chart(latest_data).mark_bar().encode(
        y=alt.Y('Plant Name:N', sort=sort_order),
        x=alt.X('Temperature (°C):Q'),
        tooltip=['Plant Name:N', 'Temperature (°C):Q'],
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='greens')
    ).properties(
        title='Latest Temperature of Plants',
        width=600
    )
    return latest_temp_readings


def get_latest_soil_moisture_readings(plants: DataFrame, sort_ascending):
    """
    Returns an altair bar chart that shows the latest soil moisture readings for each plant.
    """
    latest_data = get_latest_data(plants)

    latest_data["Plant Name"] = latest_data[["plant_name"]]
    latest_data["Soil Moisture (%)"] = latest_data[[
        "soil_moisture"]]

    latest_data = latest_data[["Plant Name", "Soil Moisture (%)"]]

    sort_order = "x" if sort_ascending else "-x"

    latest_temp_readings = alt.Chart(latest_data).mark_bar().encode(
        y=alt.Y('Plant Name:N', sort=sort_order),
        x=alt.X('Soil Moisture (%):Q'),
        tooltip=['Plant Name:N', 'Soil Moisture (%):Q'],
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='browns')
    ).properties(
        title='Latest Soil Moisture Percentage of Plants',
        width=600
    )
    return latest_temp_readings


# [TODO]: Create line chart for below function.

def get_temperature_over_time(plants: DataFrame):
    """
    Returns an altair line chart that shows the temperature readings for each plant over time.
    """
    plants["Time"] = pd.to_datetime(plants["at"]).dt.hour
    plants["Plant Name"] = plants[["plant_name"]]

    temp_over_time = plants.groupby(["Plant Name", "Time"])[
        "temperature"].mean().reset_index()

    line_chart = alt.Chart(temp_over_time).mark_line().encode(
        x=alt.X('Time', title='Time (hr)').scale(zero=False),
        y=alt.Y('temperature:Q', title='Temperature °C').scale(zero=False),
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='greens')
    ).properties(
        title='Temperature of Plants over time'
    )
    return line_chart


# [TODO]: Create line chart for below function.

def get_soil_moisture_over_time(plants: DataFrame):
    """
    Returns an altair line chart that shows the soil moisture readings for each plant over time.
    """
    plants["Time"] = pd.to_datetime(plants["at"]).dt.hour
    plants["Plant Name"] = plants[["plant_name"]]

    moisture_over_time = plants.groupby(["Plant Name", "Time"])[
        "soil_moisture"].mean().reset_index()

    line_chart = alt.Chart(moisture_over_time).mark_line().encode(
        x=alt.X('Time', title='Time (hr)').scale(zero=False),
        y=alt.Y('soil_moisture:Q', title='Soil Moisture (%)').scale(zero=False),
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='browns')
    ).properties(
        title='Soil Moisture Percentage of Plants over time'
    )
    return line_chart


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    sort_ascending_temp = st.sidebar.checkbox(
        "Ascending Temperature", True)

    latest_temp_readings = get_latest_temperature_readings(
        plants, sort_ascending_temp)

    get_temperature_over_time(plants)
