"""
Tests for the extract script.
"""

import pytest

from extract import get_number_of_plants, connect_to_plant_ids
from errors import APIError


def test_connect_to_plant_ids(requests_mock):
    """tests loads correct weather description"""

    api_plants = "https://data-eng-plants-api.herokuapp.com/plants/"
    total_num_plants = 0
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/plants/0", status_code=200)
    response = connect_to_plant_ids(total_num_plants, api_plants)

    assert response == []


def test_connect_to_plant_ids_raise_404_error(requests_mock):

    api_plants = "https://data-eng-plants-api.herokuapp.com/plants/"
    total_num_plants = 2
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/plants/1", status_code=404)
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/plants/2", status_code=404)
    with pytest.raises(APIError) as exception:
        connect_to_plant_ids(total_num_plants, api_plants)

    assert exception.value.message == {
        'error': True, 'message': 'URL invalid.'}


def test_get_number_of_plants(requests_mock):
    """tests loads correct weather description"""

    api_index = "https://data-eng-plants-api.herokuapp.com/"
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/", status_code=200, json={'plants_on_display': 49, 'success': 'Liverpool Natural History Museum - Plants API is running'})
    response = get_number_of_plants(api_index)

    assert response == 51
