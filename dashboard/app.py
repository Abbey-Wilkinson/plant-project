"""
Streamlit app for plants.
"""
from os import environ

from dotenv import load_dotenv
import pandas as pd
import streamlit as st

from database import get_database_connection, load_all_plant_data
from utilities import get_average_soil_moisture


def get_header_metrics() -> None:
    """Gets the main headers and displays them."""
    head_cols = st.columns(3)
    with head_cols[0]:
        st.metric("Total Number of Plants :herb:",
                  len(selected_plants))
    with head_cols[1]:
        st.metric("Average Soil Moisture: :potted_plant:",
                  get_average_soil_moisture(plants))


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    st.title("Plant Sensors Dashboard")

    selected_plants = st.sidebar.multiselect("Selected Plants",
                                             plants["plant_name"].unique(),
                                             default=plants["plant_name"].unique())

    if selected_plants:

        get_header_metrics()

    st.table(plants)
