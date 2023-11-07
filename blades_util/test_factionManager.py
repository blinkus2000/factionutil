# test_factionManager.py
import pytest
from blades_util.factionTable import FactionTable
from blades_util.factionManager import FactionManager

# Assuming you have a test JSON file with test factions
TEST_JSON_PATH = 'factions.json'


class TestFactionManager:
    @pytest.fixture
    def faction_table(self):
        # Setup the FactionTable with a path to the test JSON
        return FactionTable(TEST_JSON_PATH)

    @pytest.fixture
    def manager(self, faction_table):
        # Setup the FactionManager with the faction table
        return FactionManager(faction_table)

    @pytest.fixture
    def factions(self, faction_table):
        # Setup the factions with the faction table
        return faction_table.factions

    def test_initialize_weights(self, manager):
        # Check if weights are initialized correctly
        weights = manager.initialize_weights()
        for faction_name, (most_liked, least_liked) in weights.items():
            # Check if most_liked and least_liked are valid faction names
            assert most_liked in manager.faction_table.faction_names
            assert least_liked in manager.faction_table.faction_names

    def test_update_weights(self, manager, factions):
        # Update faction opinions and then update weights
        manager.faction_table.update_faction_opinion('The Billhooks', 'The Crows', 3)
        manager.update_weights()
        weights = manager.weights
        # Check if the weights have been updated correctly
        assert weights['The Crows'][0] == 'The Billhooks'  # Most liked should be 'The Billhooks' now
        assert factions['The Billhooks'].action() == 0  # Acted should still be 0

    def test_calculate_weight(self, manager):
        # Calculate weight for a faction
        manager.faction_table.update_faction_opinion('The Billhooks', 'The Crows', 3)
        manager.update_weights()
        weight = manager.calculate_weight('The Crows')
        # Check if the weight is calculated correctly
        assert weight == 3  # Since acted is 0, weight should be the opinion value

    def test_choose_acting_factions(self, manager):
        # Choose acting factions
        acting_factions = manager.choose_acting_factions()
        # Check if the chosen factions are valid
        for faction in acting_factions:
            assert faction in manager.faction_table.faction_names

    def test_run_faction_action(self, manager):
        manager.faction_table.seed_the_relationship_table()

        print()

        opinions_total = []
        for i in range(1, 100, 1):
            print(f'week {i}, this was the faction activity in duskvol:')
            print("-------------")
            results, new_opinions = manager.run_faction_actions()
            opinions_total.extend(new_opinions)
            for result in results:
                print(result)
            print("-------------")
            print(
                "Could you write a few articles for the Duskvol chronicle related to this activity,fill in how the faction actually acted when they helped out or moved against, this is for the game Blades in the Dark.")
            print("-------------")

        def categorize_opinions(opinions):
            # Define the range buckets
            buckets = [0] * 7

            def normalize_opinion(opinion_to_normalize):
                # Clamp the opinion to be within -3 to 3
                clamped_opinion = max(min(opinion_to_normalize, 3), -3)
                # Convert to integer to strip off the decimal part
                normalized_opinion = int(clamped_opinion)
                return normalized_opinion

            # Categorize each opinion into a bucket
            for opinion in opinions:
                normalized_ = normalize_opinion(opinion)
                buckets[normalized_ + 3] += 1
            return buckets

        # In your test function, after running the actions:
        opinion_buckets = categorize_opinions(opinions_total)
        for i in range(0, len(opinion_buckets), 1):
            bucket = i - 3
            count = opinion_buckets[i]
            print(f"{bucket}: {count}")

    # More tests can be added to cover additional scenarios and edge cases.
