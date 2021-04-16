import numpy as np
import json


def validate_inputs(data) -> None:
    if "number_of_rooms" not in data:
        raise ValueError("Mandatory field 'Number of rooms' is missing")
    if "area" not in data:
        raise ValueError("Mandatory field 'Area' is missing")
    if "floor_on" not in data:
        raise ValueError("Mandatory field 'Floor on' is missing")
    if "floors_total" not in data:
        raise ValueError("Mandatory field 'Total floors' is missing")
    if "district" not in data:
        raise ValueError("Mandatory field 'District' is missing")


def district_encoding(district_string) -> list:
    """Encodes the name of the district into a list of values after dummy encoding"""
    district_list = ['Akmenės r. sav.', 'Alytus', 'Antakalnis', 'Fabijoniškės', 'Jeruzalė',
       'Jonavos r. sav.', 'Justiniškės', 'Karoliniškės', 'Kaunas',
       'Kauno r. sav.', 'Klaipėda', 'Klaipėdos r. sav.', 'Kėdainių m.',
       'Mažeikių m.', 'Naujamiestis', 'Naujininkai', 'Panevėžio r. sav.',
       'Panevėžys', 'Pašilaičiai', 'Pilaitė', 'Senamiestis', 'Utenos m.',
       'Vilnius', 'Viršuliškės', 'Šeškinė', 'Šiauliai', 'Šilutės m.',
       'Žirmūnai', 'Žvėrynas']
    return_list = []
    for district in district_list:
        if district == district_string:
            return_list.append(1)
        else:
            return_list.append(0)
    return return_list


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
        enc = district_encoding(input_datum["district"])
        requests = [
            input_datum["number_of_rooms"],
            input_datum["area"],
            input_datum["floor_on"],
            input_datum["floors_total"],
        ]

        requests_returned = requests + enc
        requests_returned = [requests_returned]

    return np.asarray(requests_returned)