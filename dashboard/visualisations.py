"""
Functions to visualise data on streamlit.
"""
import altair as alt
from dotenv import load_dotenv
from pandas import DataFrame

from database import get_database_connection, load_all_plant_data
from utilities import get_latest_data


def get_latest_temperature_readings(plants: DataFrame, sort_ascending):
    """
    Returns an altair bar chart that shows the latest temperature readings for each plant.
    """
    latest_data = get_latest_data(plants)

    latest_data["Plant Name"] = latest_data[["plant_name"]]
    latest_data["Temperature"] = latest_data[["temperature"]]

    latest_data = latest_data[["Plant Name", "Temperature"]]
    print(latest_data)

    sort_order = "x" if sort_ascending else "-x"

    latest_temp_readings = alt.Chart(latest_data).mark_bar().encode(
        y=alt.Y('Plant Name:N', sort=sort_order),
        x=alt.X('Temperature:Q'),
        tooltip=['Plant Name:N', 'Temperature:Q'],
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
    latest_data["Soil Moisture Percentage"] = latest_data[["soil_moisture"]]

    latest_data = latest_data[["Plant Name", "Soil Moisture Percentage"]]
    print(latest_data)

    sort_order = "x" if sort_ascending else "-x"

    latest_temp_readings = alt.Chart(latest_data).mark_bar().encode(
        y=alt.Y('Plant Name:N', sort=sort_order),
        x=alt.X('Soil Moisture Percentage:Q'),
        tooltip=['Plant Name:N', 'Soil Moisture Percentage:Q'],
        color=alt.Color('Plant Name:N', legend=None).scale(scheme='greens')
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
    pass


# [TODO]: Create line chart for below function.

def get_soil_moisture_over_time(plants: DataFrame):
    """
    Returns an altair line chart that shows the soil moisture readings for each plant over time.
    """
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    latest_temp_readings = get_latest_temperature_readings(plants)
