from typing import Dict, Tuple, List


def convert_dict(dict_data: Dict[Tuple[str, str], float]) -> List[str]:
    first_strings = []

    for (first, second), value in dict_data.items():
        first_strings.append(first)
    return list(set(first_strings))


def get_row_as_list(row: str, dict_data: Dict[Tuple[str, str], float]) -> List[float]:
    returnVal = []
    for (first, second), value in dict_data.items():
        if first == row:
            returnVal.append(value)
    return returnVal
