"""
Extract script for the plants pipeline.
"""
from time import perf_counter

import requests
from requests.exceptions import Timeout, HTTPError
import pandas as pd

from errors import APIError

SUCCESS_CODE = 200
TIMEOUT = 20
LOOP_INCLUSIVE_NUMBER = 2
BAD_REQUEST = 400
PAGE_NOT_FOUND = 404
REQUEST_TIMED_OUT = 408
STARTING_ID = 1


def get_number_of_plants(api_index: str):
    """
    Finds the number of plants which are on display.
    """

    try:
        response = requests.get(f"{api_index}", timeout=TIMEOUT)
        data = response.json()

        number_of_plants = data["plants_on_display"]

        # add 2 because id 0 and 50 are the same, so we start from 1
        # and go to 51 since loops aren't inclusive on the last number
        return number_of_plants + LOOP_INCLUSIVE_NUMBER

    except KeyError as exc:
        raise APIError({"error": True,
                        "message": "No key 'plants_on_display' found."}, BAD_REQUEST) from exc
    except ConnectionError as exc:
        raise APIError({"error": True,
                        "message": "Connection failed."}, BAD_REQUEST) from exc
    except Timeout as exc:
        raise APIError({"error": True,
                        "message": "Timed out."}, REQUEST_TIMED_OUT) from exc
    except HTTPError as exc:
        raise APIError({"error": True,
                        "message": "URL invalid."}, PAGE_NOT_FOUND) from exc


def connect_to_plant_ids(total_num_plants: int, api_plants: str):
    """
    Fetches the data required for each plant.
    """
    try:

        plant_data = []
        for plant_id in range(STARTING_ID, total_num_plants):
            response = requests.get(f'{api_plants}{plant_id}', timeout=TIMEOUT)

            if response.status_code == SUCCESS_CODE:
                print(plant_id)
                data = response.json()
                wanted_data = {
                    "plant_id": data["plant_id"],
                    "recording_taken": data["recording_taken"],
                    "last_watered": data["last_watered"],
                    "soil_moisture": data["soil_moisture"],
                    "temperature": data["temperature"]
                }

                plant_data.append(wanted_data)

            # missing plants should be skipped if not there,
            # not raise an error unless id is in certain range
            elif (plant_id < total_num_plants and
                  plant_id > STARTING_ID):
                continue
            else:
                raise HTTPError

        return plant_data

    except ConnectionError as exc:
        raise APIError({"error": True,
                        "message": "Connection failed."}, BAD_REQUEST) from exc
    except Timeout as exc:
        raise APIError({"error": True,
                        "message": "Timed out."}, REQUEST_TIMED_OUT) from exc
    except HTTPError as exc:
        raise APIError({"error": True,
                        "message": "URL invalid."}, PAGE_NOT_FOUND) from exc


def convert_to_pd_dataframe(all_plant_data: list[dict]) -> pd.DataFrame:
    """
    Converts the list of all plant dictionaries into a pandas DataFrame.
    """

    plants_df = pd.DataFrame(all_plant_data)
    plants_df = plants_df.fillna("N/A")
    return plants_df


if __name__ == "__main__":

    API_INDEX = "https://data-eng-plants-api.herokuapp.com/"
    API_PLANTS = "https://data-eng-plants-api.herokuapp.com/plants/"

    plants_time = perf_counter()

    print("Getting total number of plants...")
    sum_of_plants = get_number_of_plants(API_INDEX)

    print("Getting plant data for each plant...")
    plants = connect_to_plant_ids(sum_of_plants, API_PLANTS)

    print("Converting into DataFrame...")
    df = convert_to_pd_dataframe(plants)

    df.to_csv("sample.csv", index=False)

    print(f"Extract phase complete --- {perf_counter() - plants_time}s.")
