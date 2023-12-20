"""
Script containing tests for daily_extract.
"""
import datetime

from unittest.mock import MagicMock

from daily_extract import extract_from_rds, create_condition_dicts


def test_extract_from_rds_works():
    """
    Tests that the extract_from_rds function does successfully extract.
    """

    mock_connection = MagicMock()
    mock_fake_execute = MagicMock()

    mock_execute = mock_connection.execute

    mock_connection.execute.return_value = mock_fake_execute
    mock_fetch = mock_fake_execute.fetchall
    mock_fetch.return_value = [(2, datetime.datetime(2023, 12, 19, 11, 0, 45),
                                25.22258419783465, 12.013140983634887,
                                datetime.datetime(2023, 12, 18, 13, 54, 32), 1),
                               (3, datetime.datetime(2023, 12, 19, 11, 0, 46),
                                31.762604085532303, 9.08111140376697,
                                datetime.datetime(2023, 12, 18, 14, 10, 54), 2)]

    results = extract_from_rds(mock_connection)

    assert mock_execute.call_count == 2
    assert mock_fetch.call_count == 1
    assert results == [(2, datetime.datetime(2023, 12, 19, 11, 0, 45),
                        25.22258419783465, 12.013140983634887,
                        datetime.datetime(2023, 12, 18, 13, 54, 32), 1),
                       (3, datetime.datetime(2023, 12, 19, 11, 0, 46),
                        31.762604085532303, 9.08111140376697,
                        datetime.datetime(2023, 12, 18, 14, 10, 54), 2)]


def test_turn_into_dicts_valid_input():
    """
    Tests that the create_condition_dicts function returns a correct dictionary, given valid data.
    """

    test_input = [(2, datetime.datetime(2023, 12, 19, 11, 0, 45),
                   25.22258419783465, 12.013140983634887,
                   datetime.datetime(2023, 12, 18, 13, 54, 32), 1)]

    assert create_condition_dicts(test_input) == [{'at': datetime.datetime(2023, 12, 19, 11, 0, 45),
                                                   'soil_moisture': 25.22258419783465,
                                                   'temp': 12.013140983634887, 'last_watered':
                                                   datetime.datetime(
                                                  2023, 12, 18, 13, 54, 32),
        'plant_id': 1}]


def test_turn_into_dicts_empty_input():
    """
    Tests that the create_condition_dicts function returns an empty list if given empty input.
    """

    assert create_condition_dicts([]) == []


def test_turn_into_dicts_invalid_input():
    """
    Tests that the create_condition_dicts function returns an empty list if given invalid input.
    """

    test_input = [(2, datetime.datetime(2023, 12, 19, 11, 0, 45))]
    assert create_condition_dicts(test_input) == []
