import pytest
from utils.input_processor import process_input


def validate_input_number_of_rooms():
    test_inputs = {
        [{"area": 31, "floor_on": 5, "floors_total": 9, "district": "Antakalnis"}]
    }
    with pytest.raises(ValueError):
        validate_inputs(test_inputs)


def validate_input_area():
    test_inputs = {
        [
            {
                "number_of_rooms": 1,
                "floor_on": 5,
                "floors_total": 9,
                "district": "Antakalnis",
            }
        ]
    }
    with pytest.raises(ValueError):
        validate_inputs(test_inputs)


def validate_input_floor_on():
    test_inputs = {
        [
            {
                "area": 31,
                "number_of_rooms": 1,
                "floors_total": 9,
                "district": "Antakalnis",
            }
        ]
    }
    with pytest.raises(ValueError):
        validate_inputs(test_inputs)


def validate_input_floors_total():
    test_inputs = {
        [{"area": 31, "number_of_rooms": 1, "floor_on": 5, "district": "Antakalnis"}]
    }
    with pytest.raises(ValueError):
        validate_inputs(test_inputs)


def validate_input_district():
    test_inputs = {
        [{"number_of_rooms": 1, "area": 31, "floor_on": 5, "floors_total": 9}]
    }
    with pytest.raises(ValueError):
        assert validate_inputs(test_inputs)


def test_encoding_district():
    test_input = "Antakalnis"
    test_encoding = [
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert district_encoding(test_input) == test_encoding


def test_process_input():
    test_encoding = [
        1,
        31,
        5,
        9,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    test_encoded_values = [
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    test_numeric_values = [1, 31, 5, 9]
    result = test_numeric_values + test_encoded_values
    assert result == test_encoding
