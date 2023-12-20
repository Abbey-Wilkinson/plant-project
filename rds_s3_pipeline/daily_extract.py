"""
Loads all the daily data from the database, 
converts it to a .csv file
and uploads it to the s3 bucket.
"""

from os import environ, remove

from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, sql, Connection
import pandas as pd
from boto3 import client

from errors import DBConnectionError

CURRENT_DATE = datetime.today()
BAD_REQUEST = 400


def get_database_connection() -> Connection:
    """
    Establishes a connection with the plants database.
    """

    try:
        print("Making new database connection")
        engine = create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}" +
            f"@{environ['DB_HOST']}/?charset=utf8")

        return engine.connect()
    except ConnectionError as exc:
        raise DBConnectionError(
            {'error': True, 'message': 'Connection Failed'}, BAD_REQUEST) from exc


def extract_from_rds(db_conn: Connection) -> list[tuple]:
    """
    Extracts all the plant condition entries from the epsilon schema.
    """

    db_conn.execute(sql.text("USE plants;"))

    query = sql.text("SELECT * FROM s_epsilon.plant_condition;")
    res = db_conn.execute(query).fetchall()

    return res


def wipe_from_rds(db_conn: Connection) -> None:
    """
    Wipes all the plant condition entries from the epsilon schema.
    """

    db_conn.execute(sql.text("USE plants;"))

    query = sql.text("DELETE * FROM s_epsilon.plant_condition;")
    db_conn.execute(query)


def create_condition_dicts(conditions: list[tuple]) -> list[dict]:
    """
    Loops through every plant condition entry and converts them into a dataframe.
    """

    plant_conditions = []
    for condition in conditions:
        if len(condition) != 6:
            print("Incorrect tuple.")
            continue

        data = {
            'at': condition[1],
            'soil_moisture': condition[2],
            'temp': condition[3],
            'last_watered': condition[4],
            'plant_id': condition[5]
        }

        plant_conditions.append(data)

    return plant_conditions


def convert_to_csv_and_upload(plant_conditions: list[dict], s3_client: client, bucket):
    """
    Converts the plant condition dataframe into a .csv file and uploads it to the s3 bucket.
    """

    df = pd.DataFrame(plant_conditions)
    df.to_csv('./plant_conditions.csv')

    s3_client.upload_file("./plant_conditions.csv", bucket,
                          f"{CURRENT_DATE.year}-{CURRENT_DATE.month}/{CURRENT_DATE.day}.csv")
    remove("./plant_conditions.csv")


if __name__ == "__main__":

    load_dotenv()

    try:
        s3 = client("s3",
                    aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

        conn = get_database_connection()
        list_of_conditions = extract_from_rds(conn)
        plant_conditions_dicts = create_condition_dicts(list_of_conditions)
        convert_to_csv_and_upload(
            plant_conditions_dicts, s3, "c9-queenbees-bucket")
    except KeyError as error:
        print("Can't connect to AWS")
        wipe_from_rds()
