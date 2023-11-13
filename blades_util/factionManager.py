from typing import Dict, Tuple, List
import random
from blades_util.factionTable import FactionTable
from blades_util.faction import Faction
from blades_util.status import Status
from blades_util.status import get_status
import random
from typing import List, Tuple


def get_faction_action(actingFaction: Faction, targetFaction: Faction, currentFeelings: float) -> float:
    # Calculate the relative power as a delta
    acting_rating = actingFaction.rating()
    target_rating = targetFaction.rating()
    relative_power = acting_rating - target_rating
    if currentFeelings < 0:
        relative_power = relative_power * -1
    chance_to_go_against_feelings = (relative_power + 10) / 100
    magnitude_of_change =min(3, 1 + random.random() * abs(currentFeelings));
    if random.random() < chance_to_go_against_feelings:
        magnitude_of_change = magnitude_of_change * -1

    return magnitude_of_change - 2


class FactionManager:
    def __init__(self, faction_table: FactionTable):
        # Initialize the manager with a reference to a FactionTable instance
        self.faction_table = faction_table
        # Initialize the weights for each faction
        self.weights = self.initialize_weights()
        self.saved_results: list[str] = None

    def initialize_weights(self) -> Dict[str, Tuple[str, str]]:
        # Create a dictionary to hold the weights for each faction
        weights = {}
        # Iterate over all factions to initialize their weights
        for faction_name in self.faction_table.faction_names:
            # Retrieve all opinions for the current faction
            opinions = self.faction_table.get_all_opinions()[faction_name]
            # Find the most liked faction based on the highest opinion value
            most_liked = max(opinions, key=opinions.get)
            # Find the least liked faction based on the lowest opinion value
            least_liked = min(opinions, key=opinions.get)
            # Initialize the weight with most liked, least liked, and acted count (0 initially)
            weights[faction_name] = (most_liked, least_liked)
        return weights

    def decay_acted_count(self) -> None:
        # Iterate over the weights dictionary
        for faction_name, faction in self.faction_table.factions.items():
            # Decrement the acted count but not below 0
            new_acted_count = max(faction.action() - 1, 0)
            # Update the weights dictionary with the new acted count
            faction.set_action(new_acted_count)

    def update_weights(self):
        # Update the weights for each faction based on the latest opinions
        for faction_name, (most_liked, least_liked) in self.weights.items():
            # Retrieve the latest opinions for the current faction
            opinions = self.faction_table.get_all_opinions()[faction_name]
            # Update the weight with the new most liked and least liked factions
            self.weights[faction_name] = (
                max(opinions, key=opinions.get),
                min(opinions, key=opinions.get)
            )

    def calculate_weight(self, faction_name: str) -> float:
        # Calculate the weight of a faction's desire to act
        acted = self.faction_table.factions[faction_name].action()
        love, hate = self.weights[faction_name]
        # Calculate the weight for love and hate, adjusted by the acted count
        love_weight = self.faction_table.get_faction_opinion(faction_name, love) / (acted + 1)
        hate_weight = self.faction_table.get_faction_opinion(faction_name, hate) / (acted + 1)
        # The total weight is the sum of the absolute values of love and hate weights
        return abs(love_weight) + abs(hate_weight)

    def choose_acting_factions(self) -> List[str]:
        # Exclude "The Players" from the list of factions that can act
        eligible_factions = [faction for faction in self.faction_table.faction_names if faction != "The Players"]

        # Calculate weights for all eligible factions
        weights = {faction: self.calculate_weight(faction) for faction in eligible_factions}
        total_weight = sum(weights.values())

        # Decide how many factions will act this turn (between 1 and 5)
        number_of_actors = random.randint(1, 5)

        chosen_factions = set()  # Use a set to avoid duplicates
        if total_weight != 0:
            while len(chosen_factions) < number_of_actors:
                # Determine the probability for each faction to act based on their weight
                probabilities = {faction: weight / total_weight for faction, weight in weights.items()}
                # Choose a faction based on their probabilities
                chosen_faction = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
                # Add the chosen faction to the set
                chosen_factions.add(chosen_faction)
        else:
            # If there are no weights at all, just choose actors at random from eligible factions
            # Ensure unique factions are chosen using random.sample
            chosen_factions = set(random.sample(eligible_factions, k=min(number_of_actors, len(eligible_factions))))

        return list(chosen_factions)

    def determine_target_and_feelings(self, acting_faction_name: str) -> Tuple[Faction, float]:
        # Retrieve all opinions for the acting faction
        opinions = self.faction_table.get_all_opinions()[acting_faction_name]

        # Find the faction with the strongest feelings (highest absolute opinion value)
        target_faction_name = max(opinions, key=lambda k: abs(opinions[k]))
        # Get the current feelings (opinion value) for that faction
        current_feelings = opinions[target_faction_name]

        # Retrieve the target Faction object
        target_faction = self.faction_table.factions[target_faction_name]

        return target_faction, current_feelings

    def build_faction_actions(self) -> List[Tuple[Faction, Faction, float]]:
        # Get the list of factions that will act this turn
        acting_factions = self.choose_acting_factions()

        # Initialize an empty list to hold the action tuples
        faction_actions = []

        # Iterate over each acting faction
        for acting_faction in acting_factions:
            # Determine the target faction and current feelings
            # This is an example, you'll need to implement the logic to get these values
            target_faction, current_feelings = self.determine_target_and_feelings(acting_faction)

            acting_faction_obj = self.faction_table.factions[acting_faction]
            # Get the action value using the get_faction_action method
            action_value = get_faction_action(acting_faction_obj, target_faction, current_feelings)

            # Append the tuple to the list of faction actions
            faction_actions.append((acting_faction_obj, target_faction, action_value))

        # Return the list of faction actions
        return faction_actions

    def run_faction_actions(self) -> Tuple[List[str],List[float]]:
        self.decay_acted_count()
        actions = self.build_faction_actions()
        results = []
        new_opinions = []
        for acting_faction, target_faction, opinion_change in actions:
            # Update faction opinion based on the action
            self.faction_table.update_faction_opinion(acting_faction_name=acting_faction.name,
                                                      target_faction_name=target_faction.name,
                                                      opinion_change=opinion_change)

            # Increment the acted_count for the acting faction by 2
            most_liked, least_liked = self.weights[acting_faction.name]
            self.weights[acting_faction.name] = (most_liked, least_liked)
            acting_faction.set_action(2 + acting_faction.action())

            # Build the result string
            new_opinion = self.faction_table.get_faction_opinion(target_faction.name, acting_faction.name)
            status = get_status(new_opinion)
            action_type = "helped out" if opinion_change > 0 else "moved against"
            result = f"{acting_faction.name} {action_type} {target_faction.name}." \
                     f" {status.get_description_for(acting_faction.name)}"
            results.append(result)
            new_opinions.append(new_opinion)

        return results, new_opinions



