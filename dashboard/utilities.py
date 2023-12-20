"""
Utility functions for the streamlit app.
"""
from dotenv import load_dotenv
import numpy
import pandas as pd

from database import get_database_connection, load_all_plant_data


def get_average_soil_moisture(df: pd.DataFrame) -> numpy.float64:
    """
    Returns the average soil moisture from all of the plants combined.
    """
    return df["soil_moisture"].mean().round(2)


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    average_soil_moisture = get_average_soil_moisture(plants)

    print(type(average_soil_moisture))
