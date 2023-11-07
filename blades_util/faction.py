import json
from collections import UserDict
from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class Faction:
    name: str
    description: str
    faction_dict: 'FactionDict'
    _hash: int = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, '_hash', hash((self.name, self.description)))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if isinstance(other, Faction):
            return self._hash == other._hash
        return False

    def rating(self) -> int:
        return self.faction_dict.rating(self)

    def action(self) -> int:
        return self.faction_dict.action(self)

    def set_rating(self, rating: int):
        self.faction_dict.set_rating(self, rating)

    def set_action(self, action: int):
        self.faction_dict.set_action(self, action)


class FactionDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rating_table: Dict[Faction, int] = {}
        self.action_table: Dict[Faction, int] = {}

    def action(self, faction: Faction) -> int:
        return self.action_table.get(faction, 0)

    def rating(self, faction: Faction) -> int:
        return self.rating_table.get(faction, 0)

    def set_action(self, faction: Faction, value: int):
        self.action_table[faction] = value

    def set_rating(self, faction: Faction, value: int):
        self.rating_table[faction] = value


# Now you can use FactionDict in place of the previous global variables
def load_factions(json_path: str) -> FactionDict:
    with open(json_path, 'r', encoding='utf-8') as file:
        factions_data = json.load(file)

    factions = FactionDict()
    for faction_info in factions_data:
        faction = Faction(name=faction_info['name'], description=faction_info['description'], faction_dict=factions)
        factions[faction.name] = faction
        factions.set_rating(faction, int(faction_info['rating']))
        factions.set_action(faction, int(faction_info['action']))
    return factions


def save_factions(json_path: str, factions: FactionDict) -> None:
    factions_data = [
        {
            "name": name,
            "rating": factions.rating(faction),
            "action": factions.action(faction),
            "description": faction.description
        }
        for name, faction in factions.items()
    ]

    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(factions_data, file, ensure_ascii=False, indent=4)
