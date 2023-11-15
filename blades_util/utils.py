from typing import Dict, Tuple, List


def convert_dict(dict_data: Dict[str, Dict[str, float]], first_str: str = None) -> List[str]:
    first_strings = set()

    for first in dict_data.keys():
        first_strings.add(first)

    sorted_list = sorted(first_strings)

    if first_str and first_str in sorted_list:
        sorted_list.remove(first_str)
        sorted_list.insert(0, first_str)

    return sorted_list


def get_row_as_list(row: str, dict_data: Dict[str, Dict[str, float]]) -> List[float]:
    returnVal = []
    dict_row = dict_data[row]
    for key, value in dict_row.items():
        returnVal.append(value)
    return returnVal


def convert_to_nested_dict(input_dict: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    return input_dict
