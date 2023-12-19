"""
Script that runs the entire pipeline.
"""

from os import environ
from time import perf_counter

from dotenv import load_dotenv
import pandas as pd

from extract import get_number_of_plants, connect_to_plant_ids, convert_to_pd_dataframe
from transform import (clean_last_watered_data, clean_recording_taken_data,
                       clean_soil_moisture_data, clean_temperature_data)
from load import get_all_info_from_table, get_database_connection, insert_data_into_database


if __name__ == "__main__":

    API_INDEX = "https://data-eng-plants-api.herokuapp.com/"
    API_PLANTS = "https://data-eng-plants-api.herokuapp.com/plants/"

    plants_time = perf_counter()

    print("Getting total number of plants...")
    total_num_plants = get_number_of_plants(API_INDEX)

    print("Getting plant data for each plant...")
    plants = connect_to_plant_ids(total_num_plants, API_PLANTS)

    print("Converting into DataFrame...")
    df = convert_to_pd_dataframe(plants)

    df.to_csv("sample.csv", index=False)

    print(f"Extract phase complete --- {perf_counter() - plants_time}s.")

    plants_time = perf_counter()
    df = pd.read_csv("sample.csv")

    print("Cleaning data...")
    df = clean_recording_taken_data(df)

    df = clean_last_watered_data(df)

    df = clean_soil_moisture_data(df)

    df = clean_temperature_data(df)

    df.to_csv("transformed_test.csv", index=False)
    print(f"Transform phase complete --- {perf_counter() - plants_time}s.")

    load_dotenv()

    load_time = perf_counter()

    conn = get_database_connection()

    df = pd.read_csv("transformed_test.csv")

    rows = df.to_dict('records')

    insert_data_into_database(conn, rows)

    all_info = get_all_info_from_table(conn)

    print(f"Load phase complete --- {perf_counter() - load_time}s.")
    print(f"Pipeline complete --- {perf_counter() - plants_time}s.")
