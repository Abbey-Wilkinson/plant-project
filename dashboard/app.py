"""
Streamlit app for plants.
"""
from os import environ

from dotenv import load_dotenv
from pandas import DataFrame
import streamlit as st
from boto3 import client

from parquet_extract import get_parquet, download_parquet_files, convert_to_df, remove_old_files
from database import (get_database_connection,
                      load_all_plant_data, merge_long_and_short_dataframes)
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


def get_temperature_warning_metrics(critical_temp: str) -> None:
    """
    Gets the main temperature warnings and displays them at the top.
    """
    st.warning(
        f'''WARNING! The following plants are in CRITICAL TEMPERATURE CONDITION:
        \n\n{critical_temp}''',
        icon="⚠️")


def get_soil_moisture_warning_metrics(critical_moisture: str) -> None:
    """
    Gets the main soil moisture warnings and displays them at the top.
    """
    st.warning(
        f'''WARNING! The following plants are in CRITICAL SOIL MOISTURE CONDITION:
        \n\n{critical_moisture} \n\n PLEASE WATER ASAP!''', icon="⚠️")


def get_header_metrics(plants_df: DataFrame, selected: list, names_selected: list) -> None:
    """
    Gets the main headers and displays them.
    """
    head_cols = st.columns(3)
    with head_cols[0]:
        st.metric("Total Number of Plants Selected :herb:",
                  len(selected))
    with head_cols[1]:
        st.metric("Average Soil Moisture: :potted_plant:",
                  get_average_soil_moisture(plants_df[names_selected]))
    with head_cols[2]:
        st.metric("Average Temperature: :thermometer:",
                  f'{get_average_temperature(plants_df[names_selected])}°C')
    st.divider()


def get_main_body(plants_df: DataFrame,
                  merged_df: DataFrame,
                  selected_names: list,
                  all_selected_names: list,
                  temp_sort: bool, mois_sort: bool) -> None:
    """
    Gets the main body charts and displays them.
    """
    body_cols = st.columns(2)

    with body_cols[0]:
        st.altair_chart(get_latest_temperature_readings(
            plants_df[selected_names], temp_sort), use_container_width=True)

        st.altair_chart(get_temperature_over_time(
            merged_df[all_selected_names]), use_container_width=True)

    with body_cols[1]:
        st.altair_chart(get_latest_soil_moisture_readings(
            plants_df[selected_names], mois_sort), use_container_width=True)

        st.altair_chart(get_soil_moisture_over_time(
            merged_df[all_selected_names]), use_container_width=True)


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    download_parquet_files(s3, get_parquet(s3))

    long_plants = convert_to_df()

    remove_old_files()

    plants = load_all_plant_data(conn)

    merged = merge_long_and_short_dataframes(long_plants, plants)
    merged["plant_name"] = merged["plant_name"].dropna()

    st.set_page_config(layout="wide")

    st.title(":cactus: Plant Sensors Dashboard :cactus:")

    st.sidebar.metric("Total Number of Plants in Museum :herb:",
                      len(plants["plant_name"].unique()))
    st.sidebar.divider()

    selected_plants = get_selected_plants(plants, "")
    all_selected_plants = get_selected_plants(merged, "for Long Term Data")

    name_in_selected_plants = get_names_of_selected_plants(
        plants, selected_plants)
    all_name_in_selected_plants = get_names_of_selected_plants(
        merged, all_selected_plants)

    st.sidebar.divider()

    CRITICAL_TEMP_PLANTS = get_names_of_critical_temp_plants(plants)

    st.sidebar.subheader("Latest Temperature Readings:")
    sort_ascending_temp = st.sidebar.checkbox(
        "Ascending Temperature", True)
    st.sidebar.divider()

    st.sidebar.subheader("Latest Soil Moisture Percentage Readings")
    sort_ascending_moisture = st.sidebar.checkbox(
        "Ascending Soil Moisture Percentage", True)

    if CRITICAL_TEMP_PLANTS:

        get_temperature_warning_metrics(CRITICAL_TEMP_PLANTS)

    CRITICAL_SOIL_MOISTURE_PLANTS = get_names_of_critical_soil_moisture_plants(
        plants)

    if CRITICAL_SOIL_MOISTURE_PLANTS:

        get_soil_moisture_warning_metrics(CRITICAL_SOIL_MOISTURE_PLANTS)

    if selected_plants:

        get_header_metrics(plants,
                           selected_plants,
                           name_in_selected_plants)

        get_main_body(plants,
                      merged,
                      name_in_selected_plants,
                      all_name_in_selected_plants,
                      sort_ascending_temp,
                      sort_ascending_moisture)
