"""
Transform script for the plants pipeline.
"""
import pandas as pd
from time import perf_counter

MINIMUM_SOIL_MOISTURE = 0
MAXIMUM_SOIL_MOISTURE = 55
MINIMUM_TEMPERATURE = 5
MAXIMUM_TEMPERATURE = 50


def clean_recording_taken_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the recording taken column from the DataFrame and
    drops any NaN values once values converted to datetimes.
    """

    df["recording_taken_bool"] = pd.to_datetime(
        df["recording_taken"], errors="coerce").notna()
    df = df.drop(df[df.recording_taken_bool == False].index)

    df = df.drop(columns=["recording_taken_bool"])

    return df


def clean_last_watered_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the last watered column from the DataFrame and
    drops any NaN values once values converted to datetimes.
    """

    df["last_watered"] = pd.to_datetime(
        df["last_watered"], errors="coerce")

    df = df.dropna()

    return df


def clean_soil_moisture_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clears all invalid soil moistures from the DataFrame.
    """

    df["soil_moisture"] = pd.to_numeric(
        df["soil_moisture"], errors="coerce")
    df = df.drop(df[df.soil_moisture < MINIMUM_SOIL_MOISTURE].index)
    df = df.drop(df[df.soil_moisture > MAXIMUM_SOIL_MOISTURE].index)

    df = df.dropna()

    return df


def clean_temperature_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clears all invalid temperatures from the DataFrame.
    """

    df["temperature"] = pd.to_numeric(
        df["temperature"], errors="coerce")
    df = df.drop(df[df.temperature < MINIMUM_TEMPERATURE].index)
    df = df.drop(df[df.temperature > MAXIMUM_TEMPERATURE].index)

    df = df.dropna()

    return df


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
