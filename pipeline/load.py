"""
Loads the cleaned data into an AWS RDS database.
"""

from os import environ
from time import perf_counter

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, sql

from errors import DBConnectionError

BAD_REQUEST = 400


def get_database_connection():
    """
    Establishes a database connection to the database specified.
    """

    try:
        engine = create_engine(f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}" +
                               f"@{environ['DB_HOST']}/?charset=utf8")

        return engine.connect()

    except ConnectionError as exc:
        raise DBConnectionError(
            {'error': True, 'message': 'Connection Failed'}, BAD_REQUEST) from exc


def get_all_info_from_table(db_conn):
    """
    Returns all of the information from the plant condition table from an sql query.
    """

    db_conn.execute(sql.text("USE plants;"))

    query = sql.text("SELECT * FROM s_epsilon.plant_condition;")

    db_conn.execute(sql.text("COMMIT;"))
    res = db_conn.execute(query).fetchall()

    return res


def insert_data_into_database(db_conn, df_rows):
    """
    Inserts the cleaned data into the plant condition table of the s_epsilon schema.
    """

    db_conn.execute(sql.text("USE plants;"))

    for row in df_rows:

        query = sql.text(
            "INSERT INTO s_epsilon.plant_condition" +
            "(plant_id, at, last_watered, soil_moisture, temperature)" +
            "VALUES (:plant_id, :recording_taken, :last_watered, :soil_moisture, :temperature)")
        db_conn.execute(query, {"plant_id": row["plant_id"],
                                "recording_taken": row["recording_taken"],
                                "last_watered": row["last_watered"],
                                "soil_moisture": row["soil_moisture"],
                                "temperature": row["temperature"]
                                })


if __name__ == "__main__":

    load_dotenv()

    plants_time = perf_counter()

    conn = get_database_connection()

    df = pd.read_csv("transformed_test.csv")

    rows = df.to_dict('records')

    insert_data_into_database(conn, rows)

    print(f"Load phase complete --- {perf_counter() - plants_time}s.")

    all_info = get_all_info_from_table(conn)
