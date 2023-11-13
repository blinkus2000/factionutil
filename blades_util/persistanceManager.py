import csv
import os.path
from typing import IO, List, Dict, Tuple

from blades_util.faction import FactionDict, save_factions
from blades_util.factionManager import FactionManager
from blades_util.factionTable import FactionTable
from blades_util.relationshipTable import RelationshipTable


def save_to(table: 'RelationshipTable', csv_file: IO[str]) -> None:
    writer = csv.writer(csv_file)
    # Write the header
    writer.writerow(['Source', 'Target', 'Opinion'])
    # Write the data
    for (source, target), opinion in table.table.items():
        writer.writerow([source, target, opinion])


def load_from(csv_file: IO[str]) -> 'RelationshipTable':
    reader = csv.reader(csv_file)
    # Skip the header
    next(reader, None)
    # Initialize an empty RelationshipTable
    keys: List[str] = []
    table_data: Dict[Tuple[str, str], float] = {}
    for row in reader:
        source, target, opinion = row
        keys.extend([source, target])
        table_data[(source, target)] = float(opinion)
    # Remove duplicates from keys
    unique_keys = list(set(keys))
    # Create a new RelationshipTable
    new_table = RelationshipTable(unique_keys)
    new_table.table = table_data
    return new_table


def get_faction_manager(json_file: str, relationship_csv: str) -> FactionManager:
    with open(relationship_csv, mode='r', newline='', encoding='utf-8') as csv_file:
        relationship_table = load_from(csv_file)
    faction_table = FactionTable(json_file, relationship_table)
    return FactionManager(faction_table)


def save_faction_manager(manager: FactionManager, json_file: str, relationship_csv: str, events_txt: str) -> None:
    prep_file(relationship_csv)
    prep_file(json_file)
    prep_file(events_txt)
    with open(relationship_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        table: RelationshipTable = manager.faction_table.relationship_table
        save_to(table, csv_file)
    factions: FactionDict = manager.faction_table.factions
    save_factions(json_file, factions)
    with open(events_txt, mode='w', newline='', encoding='utf-8') as text_file:
        manager.saved_results


def prep_file(a_file):
    # Check if the file exists
    if os.path.exists(a_file):
        # Remove the file if it exists
        os.remove(a_file)
    # Create a new empty file
    with open(a_file, 'w') as f:
        pass  # 'pass' just means "do nothing". The file is created by opening it in write mode.
