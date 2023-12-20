"""
Streamlit app for plants.
"""
from dotenv import load_dotenv
from pandas import DataFrame
import streamlit as st

from database import get_database_connection, load_all_plant_data
from utilities import (get_selected_plants,
                       get_average_soil_moisture,
                       get_average_temperature,
                       get_names_of_selected_plants)


# [TODO]: Implement Warning Features for critical plants.

def get_warning_metrics() -> None:
    """
    Gets the main warnings and displays them at the top.
    """
    st.warning('This is a warning', icon="⚠️")


def get_header_metrics(plants: DataFrame) -> None:
    """
    Gets the main headers and displays them.
    """
    head_cols = st.columns(3)
    with head_cols[0]:
        st.metric("Total Number of Plants :herb:",
                  len(selected_plants))
    with head_cols[1]:
        st.metric("Average Soil Moisture: :potted_plant:",
                  get_average_soil_moisture(plants[name_in_selected_plants]))
    with head_cols[2]:
        st.metric("Average Temperature: :thermometer:",
                  f'{get_average_temperature(plants[name_in_selected_plants])}°C')


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    st.title("Plant Sensors Dashboard")

    selected_plants = get_selected_plants(plants)

    name_in_selected_plants = get_names_of_selected_plants(
        plants, selected_plants)

    if selected_plants:

        get_header_metrics(plants)

    st.table(plants)
