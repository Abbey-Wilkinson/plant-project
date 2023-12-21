"""
Script that extracts all of the .parquet files from the S3 bucket and concatenates them.
"""

from os import environ, path, mkdir, listdir
from time import perf_counter

import pandas as pd
import fastparquet
from dotenv import load_dotenv
from boto3 import client


FOLDER_NAME = "plant_data"


def get_parquet(s3_client: client) -> list[str]:
    """
    Returns the name of every file in our S3 bucket.
    """

    plant_data_bucket = s3_client.list_objects(
        Bucket=environ["BUCKET_NAME"])["Contents"]

    return [o["Key"] for o in plant_data_bucket]


def download_parquet_files(s3_client: client, parquet_list: list[str]) -> None:
    """
    From a list of parquet files, download all of them to the local machine.
    """

    if not path.exists(FOLDER_NAME):
        mkdir(FOLDER_NAME)

    for index, parquet in enumerate(parquet_list):
        file_name = f"{index}.parquet"
        file_path = path.join(FOLDER_NAME, file_name)
        s3_client.download_file(
            environ["BUCKET_NAME"], parquet, file_path)


def convert_to_df() -> pd.DataFrame:
    """
    Converts all of the .parquet files into a Pandas DataFrame.
    """

    long_plants_df = pd.DataFrame()

    for parquet in listdir(FOLDER_NAME):
        mini_plants_df = pd.read_parquet(
            f"{FOLDER_NAME}/{parquet}", engine="fastparquet")
        long_plants_df = pd.concat([long_plants_df, mini_plants_df], axis=0)

    return long_plants_df


if __name__ == "__main__":

    time_counter = perf_counter()
    load_dotenv()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    download_parquet_files(s3, get_parquet(s3))

    long_plants = convert_to_df()

    print(f"Long term data downloaded --- {perf_counter() - time_counter}s.")
