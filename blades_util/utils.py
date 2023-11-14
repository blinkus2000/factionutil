from typing import Dict, Tuple, List


def convert_dict(dict_data: Dict[Tuple[str, str], float], first_str: str = None) -> List[str]:
    first_strings = set()

    for (first, _), _ in dict_data.items():
        first_strings.add(first)

    sorted_list = sorted(first_strings)

    if first_str and first_str in sorted_list:
        sorted_list.remove(first_str)
        sorted_list.insert(0, first_str)

    return sorted_list


def get_row_as_list(row: str, dict_data: Dict[Tuple[str, str], float]) -> List[float]:
    returnVal = []
    for (first, second), value in dict_data.items():
        if first == row:
            returnVal.append(value)
    return returnVal


def convert_to_nested_dict(input_dict: dict[tuple[str, str], float]) -> dict[str, dict[str, float]]:
    nested_dict = {}
    for (key1, key2), value in input_dict.items():
        if key1 not in nested_dict:
            nested_dict[key1] = {}
        nested_dict[key1][key2] = value
    return nested_dict
