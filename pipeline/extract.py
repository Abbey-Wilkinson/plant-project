'''Extract script for the plants pipeline.'''
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
import pandas as pd
from time import perf_counter

from errors import APIError


def get_number_of_plants(api_index: str):
    '''Finds the number of plants which are on display.'''

    try:
        response = requests.get(f'{api_index}', timeout=5)
        data = response.json()

        number_of_plants = data['plants_on_display']
        return number_of_plants

    except KeyError:
        raise APIError({'error': True,
                        'message': 'No key 'plants_on_display' found.'}, 400)
    except ConnectionError:
        raise APIError({'error': True,
                        'message': 'Connection failed.'}, 400)
    except Timeout:
        raise APIError({'error': True,
                        'message': 'Timed out.'}, 408)
    except HTTPError:
        raise APIError({'error': True,
                        'message': 'URL invalid.'}, 404)


def connect_to_plant_ids(total_num_plants: int, api_plants: str):
    '''Fetches the data required for each plant.'''

    try:

        plants = []
        for id in range(total_num_plants):

            response = requests.get(f'{api_plants}{id}', timeout=10)

            if response.status_code == 200:

                data = response.json()
                plants.append(data)

        return plants

    except ConnectionError:
        raise APIError({'error': True,
                        'message': 'Connection failed.'}, 400)
    except Timeout:
        raise APIError({'error': True,
                        'message': 'Timed out.'}, 408)
    except HTTPError:
        raise APIError({'error': True,
                        'message': 'URL invalid.'}, 404)


def convert_to_pd_dataframe(plants:  list[dict]) -> pd.DataFrame:
    '''Converts the list of all plant dictionaries into a pandas dataframe.'''
    df = pd.DataFrame(plants)
    df = df.fillna('N/A')
    return df


if __name__ == '__main__':

    API_INDEX = 'https://data-eng-plants-api.herokuapp.com/'
    API_PLANTS = 'https://data-eng-plants-api.herokuapp.com/plants/'

    plants_time = perf_counter()

    print('Getting total number of plants...')
    total_num_plants = get_number_of_plants(API_INDEX)

    print('Getting plant data for each plant...')
    plants = connect_to_plant_ids(total_num_plants, API_PLANTS)

    print('Converting into DataFrame...')
    df = convert_to_pd_dataframe(plants)

    df.to_csv('test_output.csv')

    print(f'Extract phase complete --- {perf_counter() - plants_time}s.')
