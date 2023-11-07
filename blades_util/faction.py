import json
from dataclasses import dataclass, field
from typing import Dict

# Initialize the rating table as a global variable
RATING_TABLE: Dict['Faction', int] = {}
ACTION_TABLE: Dict['Faction', int] = {}


@dataclass(frozen=True)
class Faction:
    name: str
    description: str
    _hash: int = field(init=False, repr=False)

    def __post_init__(self):
        # Precompute the hash once since the object is immutable
        object.__setattr__(self, '_hash', hash((self.name, self.description)))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if isinstance(other, Faction):
            return self._hash == other._hash
        return False

    def rating(self):
        # Accessor method for rating
        return RATING_TABLE[self]

    def set_rating(self, value):
        RATING_TABLE[self] = value

    def action(self):
        # Accessor method for rating
        return ACTION_TABLE[self]

    def set_action(self, value):
        ACTION_TABLE[self] = value


def load_factions_raw_data(name: str, rating: int, action: int, description: str) -> Faction:
    # Create the Faction instance
    faction = Faction(name=name, description=description)
    # Set the rating in the RATING_TABLE
    RATING_TABLE[faction] = rating
    ACTION_TABLE[faction] = action
    return faction


def load_factions(json_path: str) -> Dict[str, Faction]:
    with open(json_path, 'r', encoding='utf-8') as file:
        factions_data = json.load(file)

    factions = {faction['name']: load_factions_raw_data(name=faction['name'],
                                                        rating=int(faction['rating']),
                                                        action=int(faction['action']),
                                                        description=faction['description'])
                for faction in factions_data}
    return factions


def save_factions(json_path: str, factions_to_save: Dict[str, Faction]) -> None:
    # Prepare data for JSON serialization
    factions_data = [
        {
            "name": faction.name,
            "rating": faction.rating(),
            "action": faction.action(),
            "description": faction.description
        }
        for faction in factions_to_save.values()
    ]

    # Write the data to a JSON file
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(factions_data, file, ensure_ascii=False, indent=4)