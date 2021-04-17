import numpy as np
import json
import pickle


labeler = pickle.load(open("utils/labeler.pkl", "rb"))
enc = pickle.load(open("utils/encoder.pkl", "rb"))


def validate_inputs(data) -> None:
    if "number_of_rooms" not in data:
        raise ValueError("Mandatory field 'number_of_rooms' is missing")
    if "area" not in data:
        raise ValueError("Mandatory field 'area' is missing")
    if "floor_on" not in data:
        raise ValueError("Mandatory field 'floor_on' is missing")
    if "floors_total" not in data:
        raise ValueError("Mandatory field 'floors_total' is missing")
    if "district" not in data:
        raise ValueError("Mandatory field 'district' is missing")
    elif not data["district"][0].isupper():
        data["district"] = data["district"].capitalize()


def process_input(request_data: str) -> np.array:
    """
    Decodes the data in json format that it is supplied with as an argument, extract the values of the key "inputs" within
    the file and returns it in a form of np.array
    :param request_data: the input values in a form of a json format
    :return: np.array
    """
    input_data = json.loads(request_data)["inputs"]
    requests = []

    for input_datum in input_data:
        validate_inputs(input_datum)
        district_label = labeler.transform([input_datum["district"]]).tolist()
        encoded_district_array = enc.transform([district_label]).toarray()
        encoded_district_list = encoded_district_array.reshape(-1).tolist()
        requests = [
            input_datum["number_of_rooms"],
            input_datum["area"],
            input_datum["floor_on"],
            input_datum["floors_total"],
        ]

        requests_returned = requests + encoded_district_list
        requests_returned = [requests_returned]

    return np.asarray(requests_returned)
