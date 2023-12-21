"""
Functions to visualise data on streamlit.
"""

from os import environ
from boto3 import client

import altair as alt
from dotenv import load_dotenv
import pandas as pd
from pandas import DataFrame
import streamlit as st

from database import (get_database_connection,
                      load_all_plant_data,
                      merge_long_and_short_dataframes,
                      merge_long_with_plant_name,
                      load_plant_data)
from parquet_extract import (download_parquet_files,
                             get_parquet,
                             remove_old_files,
                             convert_to_df)
from utilities import get_latest_data


def get_latest_temperature_readings(plants: DataFrame, sort_ascending) -> alt.vegalite.v5.api.Chart:
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


def get_latest_soil_moisture_readings(plants: DataFrame, sort_ascending) -> alt.vegalite.v5.api.Chart:
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


def get_temperature_over_time(plants: DataFrame) -> alt.vegalite.v5.api.Chart:
    """
    Returns an altair line chart that shows the temperature readings for each plant over time.
    """
    plants["Time"] = pd.to_datetime(plants["at"]).dt.date
    plants["Plant Name"] = plants[["plant_name"]]

    temp_over_time = plants.groupby(["Plant Name", "Time"])[
        "temperature"].mean().reset_index()

    line_chart = alt.Chart(temp_over_time).mark_line().encode(
        x=alt.X('Time', title='Day').scale(zero=False),
        y=alt.Y('temperature:Q', title='Temperature °C').scale(zero=False),
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='greens')
    ).properties(
        title='Temperature of Plants over Time'
    )
    return line_chart


def get_soil_moisture_over_time(plants: DataFrame) -> alt.vegalite.v5.api.Chart:
    """
    Returns an altair line chart that shows the soil moisture readings for each plant over time.
    """
    plants["Time"] = pd.to_datetime(plants["at"]).dt.date
    plants["Plant Name"] = plants[["plant_name"]]

    moisture_over_time = plants.groupby(["Plant Name", "Time"])[
        "soil_moisture"].mean().reset_index()

    line_chart = alt.Chart(moisture_over_time).mark_line().encode(
        x=alt.X('Time', title='Day').scale(zero=False),
        y=alt.Y('soil_moisture:Q', title='Soil Moisture (%)').scale(zero=False),
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='browns')
    ).properties(
        title='Soil Moisture Percentage of Plants over Time'
    )
    return line_chart


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)
    just_plant = load_plant_data(conn)

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    download_parquet_files(s3, get_parquet(s3))

    long_plants = convert_to_df()

    remove_old_files()

    with_name = merge_long_with_plant_name(long_plants, just_plant)

    merged = merge_long_and_short_dataframes(with_name, plants)

    sort_ascending_temp = st.sidebar.checkbox(
        "Ascending Temperature", True)

    latest_temp_readings = get_latest_temperature_readings(
        plants, sort_ascending_temp)

    get_temperature_over_time(merged)
