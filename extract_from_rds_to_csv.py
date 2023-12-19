from os import environ, remove

from dotenv import load_dotenv
from sqlalchemy import create_engine, sql
import pandas as pd
from boto3 import client
from datetime import datetime

CURRENT_DATE = datetime.today()


def get_database_connection():
    print("Making new database connection")
    engine = create_engine(
        f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

    return engine.connect()


def extract_from_rds(conn) -> list[tuple]:

    conn.execute(sql.text("USE plants;"))

    query = sql.text("SELECT * FROM s_epsilon.plant_condition;")
    res = conn.execute(query).fetchall()

    return res


def create_condition_dataframe(conditions: list[tuple]) -> list[dict]:
    plant_conditions = []
    for condition in conditions:
        data = {
            'at': condition[1],
            'soil_moisture': condition[2],
            'temp': condition[3],
            'plant_id': condition[4]
        }

        plant_conditions.append(data)

    return plant_conditions


def convert_to_csv_and_upload(plant_conditions: list[dict], s3_client: client, bucket):
    df = pd.DataFrame(plant_conditions)
    df.to_csv('./plant_conditions.csv')

    s3_client.upload_file("./plant_conditions.csv", bucket,
                          f"{CURRENT_DATE.year}-{CURRENT_DATE.month}/{CURRENT_DATE.day}.csv")
    remove("./plant_conditions.csv")


if __name__ == "__main__":

    load_dotenv()

    s3 = client("s3",
                aws_access_key_id=environ["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=environ["AWS_SECRET_ACCESS_KEY"])

    conn = get_database_connection()
    conditions = extract_from_rds(conn)
    plant_conditions = create_condition_dataframe(conditions)
    convert_to_csv_and_upload(plant_conditions, s3, "c9-queenbees-bucket")
