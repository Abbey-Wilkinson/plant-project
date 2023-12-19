"""Loads the cleaned data into an AWS RDS database."""

from os import environ

from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, sql


def get_database_connection():
    """
    Establishes a database connection to the database specified.
    """
    try:
        engine = create_engine(
            f"mssql+pymssql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/?charset=utf8")

        return engine.connect()

    except ConnectionError as error:
        print(error)
    pass


def get_all_info_from_table(conn):
    """
    Returns all of the information from the plant condition table from an sql query.
    """

    # TODO: Make tables in RDS such that the query can be amended and completed.

    conn.execute(sql.text("USE plants;"))

    query = sql.text("SELECT * FROM s_epsilon.XXXXX;")

    conn.execute(sql.text("COMMIT;"))
    res = conn.execute(query).fetchall()

    return res


if __name__ == "__main__":

    load_dotenv()

    df = pd.read_csv("transformed_test.csv")

    conn = get_database_connection()

    all_info = get_all_info_from_table(conn)
    print(all_info)
