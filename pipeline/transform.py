"""
Transform script for the plants pipeline.
"""

from time import perf_counter
import pandas as pd


MINIMUM_SOIL_MOISTURE = 0
MAXIMUM_SOIL_MOISTURE = 100
MINIMUM_TEMPERATURE = 5
MAXIMUM_TEMPERATURE = 50


def clean_recording_taken_data(plants_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the recording taken column from the DataFrame and
    drops any NaN values once values converted to datetimes.
    """

    plants_df["recording_taken_bool"] = pd.to_datetime(
        plants_df["recording_taken"], errors="coerce").notna()
    plants_df = plants_df.drop(
        plants_df[plants_df.recording_taken_bool is False].index)

    plants_df = plants_df.drop(columns=["recording_taken_bool"])

    return plants_df


def clean_last_watered_data(plants_df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the last watered column from the DataFrame and
    drops any NaN values once values converted to datetimes.
    """

    plants_df["last_watered"] = pd.to_datetime(
        plants_df["last_watered"], errors="coerce")
    plants_df["last_watered"] = plants_df["last_watered"].str.replace(
        "+00:00", "")

    plants_df = plants_df.dropna()

    return plants_df


def clean_soil_moisture_data(plants_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clears all invalid soil moistures from the DataFrame.
    """

    plants_df["soil_moisture"] = pd.to_numeric(
        plants_df["soil_moisture"], errors="coerce")
    plants_df = plants_df.drop(
        plants_df[plants_df.soil_moisture < MINIMUM_SOIL_MOISTURE].index)
    plants_df = plants_df.drop(
        plants_df[plants_df.soil_moisture > MAXIMUM_SOIL_MOISTURE].index)

    plants_df = plants_df.dropna()

    return plants_df


def clean_temperature_data(plants_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clears all invalid temperatures from the DataFrame.
    """

    plants_df["temperature"] = pd.to_numeric(
        plants_df["temperature"], errors="coerce")
    plants_df = plants_df.drop(
        plants_df[plants_df.temperature < MINIMUM_TEMPERATURE].index)
    plants_df = plants_df.drop(
        plants_df[plants_df.temperature > MAXIMUM_TEMPERATURE].index)

    plants_df = plants_df.dropna()

    return plants_df


if __name__ == "__main__":

    plants_time = perf_counter()
    df = pd.read_csv("sample.csv")

    print("Cleaning data...")
    df = clean_recording_taken_data(df)

    df = clean_last_watered_data(df)

    df = clean_soil_moisture_data(df)

    df = clean_temperature_data(df)

    df.to_csv("transformed_test.csv", index=False)
    print(f"Transform phase complete --- {perf_counter() - plants_time}s.")
