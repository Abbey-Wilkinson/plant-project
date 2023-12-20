"""Establishes a connection to the database."""

from os import environ

from sqlalchemy import Connection, create_engine, sql
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv


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

    conn.execute(sql.text("USE plants;"))

    query = sql.text(
        """SELECT plant_condition.plant_condition_id,
        plant_condition.at, plant_condition.soil_moisture,
        plant_condition.temperature, plant_condition.last_watered,
        plant.plant_id, plant.plant_name,
        plant.scientific_name, botanist.botanist_id, botanist.first_name,
        botanist.surname, botanist.email, botanist.phone_number,
        origin.origin_id, origin.latitude, origin.longitude, origin.region
        FROM s_epsilon.plant_condition
        JOIN s_epsilon.plant ON s_epsilon.plant.plant_id = s_epsilon.plant_condition.plant_id
        JOIN s_epsilon.botanist ON s_epsilon.botanist.botanist_id = s_epsilon.plant.botanist_id
        JOIN s_epsilon.origin ON s_epsilon.origin.origin_id = s_epsilon.plant.origin_id;""")

    conn.execute(sql.text("COMMIT;"))
    res = conn.execute(query).fetchall()
    df = pd.DataFrame(res)

    return df


if __name__ == "__main__":

    load_dotenv()

    conn = get_database_connection()

    plants = load_all_plant_data(conn)
    print(plants)
