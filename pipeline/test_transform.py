"""Tests for the transform script."""

import pandas as pd
from pandas import Timestamp

from transform import (clean_recording_taken_data,
                       clean_last_watered_data,
                       clean_soil_moisture_data,
                       clean_temperature_data)


def test_last_watered_all_datetime():
    """
    Checks the clean_last_watered_data gets all values when valid.
    """

    filled_data = {"last_watered": ["Mon, 18 Dec 2023 13:54:32 GMT",
                                    "Tue, 19 Dec 2023 9:54:32 GMT"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_last_watered_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"last_watered": {0: Timestamp("2023-12-18 13:54:32+0000", tz="GMT"),
                                        1: Timestamp("2023-12-19 09:54:32+0000", tz="GMT")},
                       "soil_moisture": {0: 33.243289352, 1: 29.234892343}}


def test_last_watered_incorrect_values():
    """
    Checks the clean_last_watered_data gets all values when one is invalid.
    """

    filled_data = {"last_watered": ["Mon, 18 Dec 2023 13:54:32 GMT",
                                    "test hehe"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_last_watered_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"last_watered": {0: Timestamp("2023-12-18 13:54:32+0000", tz="GMT")},
                       "soil_moisture": {0: 33.243289352}}


def test_last_watered_two_incorrect_values():
    """
    Checks the clean_last_watered_data gets all values when two are invalid.
    """

    filled_data = {"last_watered": ["Mon, 30 Feb 2024 13:54:32 GMT",
                                    "test hehe"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_last_watered_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"last_watered": {},
                       "soil_moisture": {}}


def test_last_watered_no_values():
    """
    Checks the clean_last_watered_data still completes when there are no values.
    """

    filled_data = {"last_watered": [""]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_last_watered_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"last_watered": {}}


def test_recording_taken_all_datetime():
    """
    Checks the clean_recording_taken_data gets all values when valid.
    """

    filled_data = {"recording_taken": ["2023-12-19 11:00:45",
                                       "2023-12-19 11:00:46"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_recording_taken_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"recording_taken": {0: "2023-12-19 11:00:45",
                                           1: "2023-12-19 11:00:46"},
                       "soil_moisture": {0: 33.243289352, 1: 29.234892343}}


def test_recording_taken_incorrect_value():
    """
    Checks the clean_recording_taken_data gets all values when one is invalid.
    """

    filled_data = {"recording_taken": ["2023-12-19 11:00:45",
                                       "test eheh"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_recording_taken_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"recording_taken": {0: "2023-12-19 11:00:45"},
                       "soil_moisture": {0: 33.243289352}}


def test_recording_taken_two_incorrect_values():
    """
    Checks the clean_recording_taken_data gets all values when two are invalid.
    """

    filled_data = {"recording_taken": ["2024-02-30 11:00:45",
                                       "test hehe"], "soil_moisture": [33.243289352, 29.234892343]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_recording_taken_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"recording_taken": {},
                       "soil_moisture": {}}


def test_recording_taken_no_values():
    """
    Checks the clean_recording_taken_data function still completes when there are no values.
    """

    filled_data = {"recording_taken": [""]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_recording_taken_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"recording_taken": {}}


def test_soil_moisture_valid_values():
    """
    Checks the clean_soil_moisture_data function completes when all values are valid.
    """

    filled_data = {"soil_moisture": [18.722501744094487, 25.753327753412194],
                   "recording_taken": ["2023-12-19 12:50:49", "2023-12-19 12:50:51"]}
    df = pd.DataFrame(data=filled_data).reset_index(drop=True)

    df = clean_soil_moisture_data(df)

    dict_df = df.to_dict()
    assert dict_df == {"soil_moisture": {0: 18.722501744094487, 1: 25.753327753412194},
                       "recording_taken": {0: "2023-12-19 12:50:49", 1: "2023-12-19 12:50:51"}}
