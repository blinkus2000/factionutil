import os.path
from pathlib import Path
from typing import Dict, Tuple

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
        pass

    def generate_new_manager(self) -> Tuple[str, Dict[Tuple[str, str], float]]:
        faction_table = FactionTable(DEFAULT_JSON)
        faction_table.seed_the_relationship_table()
        self.manager = FactionManager()
        self.manager_name = 'DEFAULT'
        return self.manager_name, self.manager.faction_table.relationship_table.table

    def seed_existing_relationship_table(self) -> Dict[Tuple[str, str], float]:
        faction_table = self.manager.faction_table
        faction_table.seed_the_relationship_table()
        return faction_table.relationship_table.table

    def save_manager_as(self, name: str) -> None:
        self.manager_name = name
        csv_file, json_file = get_files_from_name(name)

        # Assuming save_faction_manager is a method that takes the manager instance,
        # and paths to the json and csv files as strings.
        save_faction_manager(self.manager, json_file.as_posix(), csv_file.as_posix())

    def load_manager(self,name: str) -> Dict[Tuple[str, str], float]:
        csv_file, json_file = get_files_from_name(name)
        self.manager = get_faction_manager(json_file.as_posix(), csv_file.as_posix())
        self.manager_name = name
        return self.manager.faction_table.relationship_table.table
