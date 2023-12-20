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


def get_latest_data(df: DataFrame):
    """
    Returns the latest data of each plant id.
    """
    latest_indices = df.groupby('plant_id')['at'].idxmax()

    latest_conditions = df.loc[latest_indices]

    return latest_conditions


def get_names_of_critical_temp_plants(df: DataFrame):
    """
    Returns the names and the temperature of the critical plants.
    """
    latest_data = get_latest_data(df)

    # Gets plants in critical condition both too high and too low.
    critical_plants = latest_data[(
        latest_data['temperature'] >= 14) | (latest_data['temperature'] <= 7)]
    critical_plants["temperature"] = critical_plants["temperature"].round(
        2)
    critical_plants = critical_plants[[
        "plant_name", "temperature"]].reset_index(drop=True)
    critical_plants_dicts = critical_plants.to_dict('records')

    plants = []

    for plant in critical_plants_dicts:
        plants.append(f'{plant["plant_name"]} ({plant["temperature"]}°C)')

    joined_plants = ", \n".join(plant for plant in plants)

    return joined_plants


def get_names_of_critical_soil_moisture_plants(df: DataFrame):
    """
    Returns the names and the temperature of the critical plants.
    """
    latest_data = get_latest_data(df)

    critical_plants = latest_data[(
        latest_data['soil_moisture'] >= 99) | (latest_data['soil_moisture'] <= 25)]

    critical_plants["soil_moisture"] = critical_plants["soil_moisture"].round(
        2)
    critical_plants = critical_plants[[
        "plant_name", "soil_moisture"]].reset_index(drop=True)

    critical_plants_dicts = critical_plants.to_dict('records')

    plants = []

    for plant in critical_plants_dicts:
        plants.append(f'{plant["plant_name"]} ({plant["soil_moisture"]})')

    joined_plants = ", \n".join(plant for plant in plants)

    return joined_plants


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    average_soil_moisture = get_average_soil_moisture(plants)

    selected_plants = get_selected_plants(plants)

    names = get_names_of_selected_plants(plants, selected_plants)

    names_of_critical_plants = get_names_of_critical_temp_plants(plants)
