"""
Streamlit app for plants.
"""
from os import environ

from dotenv import load_dotenv
import pandas as pd
import streamlit as st


def get_header_metrics() -> None:
    """Gets the main headers and displays them."""
    head_cols = st.columns(3)
    with head_cols[0]:
        st.metric("Total Number of Plants :herb:",
                  len(selected_plants))


if __name__ == "__main__":

    load_dotenv()

    plants = pd.read_csv("./../pipeline/transformed_test.csv")

    st.title("Plant Sensors Dashboard")

    selected_plants = st.sidebar.multiselect("Selected Plants",
                                             plants["plant_id"].unique(),
                                             default=plants["plant_id"].unique())

    if selected_plants:

        get_header_metrics()

    st.table(plants)
