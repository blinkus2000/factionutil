# factionTable.py

import random
import numpy as np
from blades_util.relationshipTable import RelationshipTable
from blades_util.faction import load_factions
from typing import Dict


class FactionTable:
    def __init__(self, factions_json_path: str,table: RelationshipTable = None):
        # Load factions from JSON and create a list of faction names
        self.factions = load_factions(factions_json_path)
        self.faction_names = list(self.factions.keys())
        if table is not None:
            self.relationship_table = table
        else:
            # Initialize the relationship table with faction names
            self.relationship_table = RelationshipTable(self.faction_names)

    def update_faction_opinion(self, acting_faction_name, target_faction_name, opinion_change):
        # Update the opinion of one faction about another
        self.relationship_table.updateOpinion(acting_faction_name, target_faction_name, opinion_change)

    def get_faction_opinion(self, faction_name1, faction_name2):
        # Get the opinion of one faction about another
        return self.relationship_table.get(faction_name1, faction_name2)

    def get_all_opinions(self):
        # Get a dictionary of all opinions between factions
        return {name: self.relationship_table.howIfeelAboutOthers(name) for name in self.faction_names}

    def seed_the_relationship_table(self):
        # Generate opinions for each pair of factions
        for faction1 in self.faction_names:
            for faction2 in self.faction_names:
                if faction1 != faction2:
                    # Generate a random opinion using a normal distribution centered at 0
                    opinion = int(np.random.normal(0, 1))
                    # Truncate the opinion to be within the range of -3 to 3
                    opinion = max(min(opinion, 3), -3)
                    # Set the opinion in the relationship table
                    #print(f'{faction1} feels about {faction2} with a value of {opinion}')
                    self.relationship_table.set(faction1, faction2, opinion)
