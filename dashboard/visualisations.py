"""
Functions to visualise data on streamlit.
"""
import altair as alt
import pandas as pd
from pandas import DataFrame

from utilities import get_latest_data


# [TODO]: Create bar chart for below function.

def get_latest_temperature_readings(plants: DataFrame):
    """
    Returns an altair bar chart that shows the latest temperature readings for each plant.
    """
    pass


# [TODO]: Create bar chart for below function.

def get_latest_soil_moisture_readings(plants: DataFrame):
    """
    Returns an altair bar chart that shows the latest soil moisture readings for each plant.
    """
    pass


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
