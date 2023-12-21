"""
Establishes a connection to the database.
"""
from os import environ
from boto3 import client

from sqlalchemy import Connection, create_engine, sql
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

from parquet_extract import convert_to_df, download_parquet_files, remove_old_files, get_parquet


def get_database_connection() -> Connection:
    """
    Establishes a database connection to the database specified.
    """
    try:
        engine = create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

        return engine.connect()

    except ConnectionError as error:
        print(error)


def load_all_plant_data(conn: Connection) -> DataFrame:
    """
    Loads all of the desired data in from the s_epsilon schema in the RDS.
    """
    conn.execute(sql.text("USE plants;"))

    query = sql.text(
        """SELECT plant_condition.plant_condition_id,
        plant_condition.at, plant_condition.soil_moisture,
        plant_condition.temperature, plant_condition.last_watered,
        plant.plant_id, plant.plant_name,
        plant.scientific_name
        FROM s_epsilon.plant_condition
        JOIN s_epsilon.plant ON s_epsilon.plant.plant_id = s_epsilon.plant_condition.plant_id;""")

    conn.execute(sql.text("COMMIT;"))
    res = conn.execute(query).fetchall()
    df = pd.DataFrame(res)

    df = df[["at", "soil_moisture", "temperature",
             "plant_id", "plant_name", "last_watered"]]

    return df


def load_plant_data(conn):
    conn.execute(sql.text("USE plants;"))

    query = sql.text(
        """SELECT 
        plant.plant_id, plant.plant_name,
        plant.scientific_name
        FROM s_epsilon.plant;""")

    res = conn.execute(query).fetchall()
    df = pd.DataFrame(res)

    return df


def merge_long_with_plant_name(long_plants: DataFrame, just_plant: DataFrame):

    long_plants["temperature"] = long_plants["temp"]
    with_name = pd.merge(long_plants, just_plant, on="plant_id")[[
        "at", "soil_moisture", "temperature", "plant_id", "plant_name", "last_watered"]]

    return with_name


def merge_long_and_short_dataframes(long_plants: DataFrame, plants: DataFrame):
    """
    Returns a merged dataframe.
    """
    merged = pd.concat([long_plants, plants])
    return merged


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)

    just_plant = load_plant_data(conn)

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    download_parquet_files(s3, get_parquet(s3))

    long_plants = convert_to_df()

    remove_old_files()
    with_name = merge_long_with_plant_name(long_plants, just_plant)

    merged = merge_long_and_short_dataframes(with_name, plants)
