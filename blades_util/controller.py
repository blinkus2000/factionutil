from pathlib import Path
from typing import Dict, Tuple, List

from blades_util.factionManager import FactionManager
from blades_util.factionTable import FactionTable
from blades_util.persistanceManager import save_faction_manager, get_faction_manager

DEFAULT_JSON = 'factions.json'


def get_files_from_name(name):
    parent_dir = Path(f'manager_{name}')
    parent_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
    json_file = parent_dir / f"{name}.json"
    csv_file = parent_dir / f"{name}.csv"
    return csv_file, json_file


class Controller:

    def __init__(self):
        self.manager: FactionManager = None
        self.manager_name: str = None
        self.generate_new_manager()

    # this is the default manager the UI will get on startup, the extra str returned is just the name of the manager being displayed
    def generate_new_manager(self) -> Tuple[str, Dict[Tuple[str, str], float]]:
        faction_table = FactionTable(DEFAULT_JSON)
        faction_table.seed_the_relationship_table()
        self.manager = FactionManager(faction_table)
        self.manager_name = 'DEFAULT'
        return self.manager_name, self.manager.faction_table.relationship_table.table

    # not exposed to the UI
    def seed_existing_relationship_table(self) -> Dict[Tuple[str, str], float]:
        faction_table = self.manager.faction_table
        faction_table.seed_the_relationship_table()
        return faction_table.relationship_table.table.copy()

    # there will be a safeAs button that will popup for a manger name, this will repopulate the available managers selectable list
    def save_manager_as(self, name: str) -> None:
        self.manager_name = name
        self.save_manager()

    # there will be a save button that will save the current manager as is
    def save_manager(self):
        csv_file, json_file = get_files_from_name(self.manager_name)
        # Assuming save_faction_manager is a method that takes the manager instance,
        # and paths to the json and csv files as strings.
        save_faction_manager(self.manager, json_file.as_posix(), csv_file.as_posix())

    # from the list of available managers (populated by get_available_managers()) if a player selects that manager, it will repopulate the grid
    def load_manager(self, name: str) -> Dict[Tuple[str, str], float]:
        csv_file, json_file = get_files_from_name(name)
        self.manager = get_faction_manager(json_file.as_posix(), csv_file.as_posix())
        self.manager_name = name
        return self.manager.faction_table.relationship_table.table.copy()

    # used to populate the available managers selectable list
    def get_available_managers(self) -> List[str]:
        current_dir = Path("")
        # List comprehension to filter, transform, and collect directory names
        return_val = [model_dir.name[len("manager_"):] for model_dir in current_dir.iterdir()
                      if model_dir.is_dir() and model_dir.name.startswith("manager_")]
        return return_val

    # the row labels will be prepended with an adjust button,
    # a popup with a spinner will show up to select the amount positive or negative ints, apply button on the popup will send it
    def player_adjust_faction(self, faction_name: str, amount: int) -> Dict[Tuple[str, str], float]:
        self.manager.faction_table.update_faction_opinion("The Players", faction_name, amount)
        return self.manager.faction_table.relationship_table.table.copy()

    # this is an advance one week, the results will be displayed to a console beneath everything that I can right click clear or copy to clipboard
    def advance_one_week(self) -> Tuple[List[str], Dict[Tuple[str, str], float]]:
        results, count = self.manager.run_faction_actions()
        self.save_manager()
        return results, self.manager.faction_table.relationship_table.table.copy()
