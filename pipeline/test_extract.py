"""Tests for the extract script."""
import pytest

from errors import APIError
from extract import get_number_of_plants, connect_to_plant_ids


def test_connect_to_plant_ids(requests_mock):
    """tests loads correct weather description"""

    api_plants = "https://data-eng-plants-api.herokuapp.com/plants/"
    total_num_plants = 0
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/plants/0", status_code=200)
    response = connect_to_plant_ids(total_num_plants, api_plants)

    assert response == []


def test_get_number_of_plants(requests_mock):
    """tests loads correct weather description"""

    api_index = "https://data-eng-plants-api.herokuapp.com/"
    requests_mock.get(
        "https://data-eng-plants-api.herokuapp.com/", status_code=404)
    response = get_number_of_plants(api_index)

    assert response == []
