"""
Streamlit app for plants.
"""

from os import environ

from dotenv import load_dotenv
from pandas import DataFrame
import streamlit as st
from boto3 import client

from parquet_extract import get_parquet, download_parquet_files, convert_to_df
from database import get_database_connection, load_all_plant_data
from utilities import (get_selected_plants,
                       get_average_soil_moisture,
                       get_average_temperature,
                       get_names_of_selected_plants,
                       get_names_of_critical_temp_plants,
                       get_names_of_critical_soil_moisture_plants)
from visualisations import (get_latest_temperature_readings,
                            get_latest_soil_moisture_readings,
                            get_temperature_over_time,
                            get_soil_moisture_over_time)


def get_temperature_warning_metrics(critical_temp_plants) -> None:
    """
    Gets the main temperature warnings and displays them at the top.
    """
    st.warning(
        f'WARNING! The following plants are in CRITICAL TEMPERATURE CONDITION: \n\n{critical_temp_plants}', icon="⚠️")


def get_soil_moisture_warning_metrics(critical_moisture_plants) -> None:
    """
    Gets the main soil moisture warnings and displays them at the top.
    """
    st.warning(
        f'WARNING! The following plants are in CRITICAL SOIL MOISTURE CONDITION: \n\n{critical_moisture_plants} \n\n PLEASE WATER ASAP!', icon="⚠️")


def get_header_metrics(plants: DataFrame) -> None:
    """
    Gets the main headers and displays them.
    """
    head_cols = st.columns(3)
    with head_cols[0]:
        st.metric("Total Number of Plants Selected :herb:",
                  len(selected_plants))
    with head_cols[1]:
        st.metric("Average Soil Moisture: :potted_plant:",
                  get_average_soil_moisture(plants[name_in_selected_plants]))
    with head_cols[2]:
        st.metric("Average Temperature: :thermometer:",
                  f'{get_average_temperature(plants[name_in_selected_plants])}°C')
    st.divider()


def get_main_body(plants) -> None:
    """
    Gets the main body charts and displays them.
    """
    body_cols = st.columns(2)

    with body_cols[0]:
        st.altair_chart(get_latest_temperature_readings(
            plants[name_in_selected_plants], sort_ascending_temp), use_container_width=True)

        st.altair_chart(get_temperature_over_time(
            plants[name_in_selected_plants]), use_container_width=True)

    with body_cols[1]:
        st.altair_chart(get_latest_soil_moisture_readings(
            plants[name_in_selected_plants], sort_ascending_moisture), use_container_width=True)

        st.altair_chart(get_soil_moisture_over_time(
            plants[name_in_selected_plants]), use_container_width=True)


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    download_parquet_files(s3, get_parquet(s3))

    long_plants = convert_to_df()

    plants = load_all_plant_data(conn)

    st.set_page_config(layout="wide")

    st.title("Plant Sensors Dashboard")

    st.sidebar.metric("Total Number of Plants in Museum :herb:",
                      len(plants["plant_name"].unique()))

    selected_plants = get_selected_plants(plants)

    name_in_selected_plants = get_names_of_selected_plants(
        plants, selected_plants)

    critical_temp_plants = get_names_of_critical_temp_plants(plants)

    st.sidebar.subheader("Latest Temperature Readings:")
    sort_ascending_temp = st.sidebar.checkbox(
        "Ascending Temperature", True)

    st.sidebar.subheader("Latest Soil Moisture Percentage Readings")
    sort_ascending_moisture = st.sidebar.checkbox(
        "Ascending Soil Moisture Percentage", True)

    if critical_temp_plants:

        get_temperature_warning_metrics(critical_temp_plants)

    critical_soil_moisture_plants = get_names_of_critical_soil_moisture_plants(
        plants)

    if critical_soil_moisture_plants:

        get_soil_moisture_warning_metrics(critical_soil_moisture_plants)

    if selected_plants:

        get_header_metrics(plants)

        get_main_body(plants)

    # st.table(plants)
