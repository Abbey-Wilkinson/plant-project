"""
Utility functions for the streamlit app.
"""
from dotenv import load_dotenv
from numpy import float64
from pandas import DataFrame, Series
from streamlit import sidebar

from database import get_database_connection, load_all_plant_data


def get_selected_plants(plants: DataFrame) -> list:
    """
    Returns the selected plants in the sidebar.
    By Default this returns all plants.
    """
    return sidebar.multiselect("Selected Plants",
                               plants["plant_name"].unique(),
                               default=plants["plant_name"].unique())


def get_names_of_selected_plants(plants: DataFrame, selected_plants: list) -> Series:
    """
    Returns the names of the selected plants in the sidebar.
    """
    return plants["plant_name"].isin(selected_plants)


def get_average_soil_moisture(df: DataFrame) -> float64:
    """
    Returns the average soil moisture from all of the plants combined.
    """
    return df["soil_moisture"].astype(float).mean().round(2)


def get_average_temperature(df: DataFrame) -> float64:
    """
    Returns the average temperature from all of the plants combined.
    """
    return df["temperature"].astype(float).mean().round(2)


# [TODO]: Get the plants with a temperature above 30 degrees (in critical condition).

def get_plants_with_temperature_above_30_degrees(df: DataFrame):
    """
    Returns all of the plants with a current temperature over 30 degrees.
    """
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    average_soil_moisture = get_average_soil_moisture(plants)

    print(type(average_soil_moisture))

    selected_plants = get_selected_plants(plants)
    print(type(selected_plants))

    names = get_names_of_selected_plants(selected_plants)
    print(type(names))
