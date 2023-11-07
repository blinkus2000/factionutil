# factionTableTest.py
import pytest
from blades_util.factionTable import FactionTable

# Assuming you have a test JSON file with test factions
TEST_JSON_PATH = 'factions.json'


class TestFactionTable:
    @pytest.fixture
    def faction_table(self):
        # Setup the FactionTable with a path to the test JSON
        return FactionTable(TEST_JSON_PATH)

    def test_update_faction_opinion(self, faction_table):
        # Test updating the opinion of one faction about another
        faction_table.update_faction_opinion('The Billhooks', 'The Crows', 1)
        assert faction_table.get_faction_opinion('The Crows', 'The Billhooks') == 1

    def test_get_faction_opinion(self, faction_table):
        # Test getting the opinion of one faction about another
        faction_table.update_faction_opinion('The Billhooks', 'The Crows', 2)
        assert faction_table.get_faction_opinion('The Crows', 'The Billhooks') == 2

    def test_get_all_opinions_initial_state(self, faction_table):
        # Test getting all opinions in their initial state (should be neutral/0)
        all_opinions = faction_table.get_all_opinions()
        for opinions in all_opinions.values():
            assert all(value == 0 for value in opinions.values())

    def test_get_all_opinions_after_update(self, faction_table):
        # Test getting all opinions after an update
        faction_table.update_faction_opinion('The Billhooks', 'The Crows', -1)
        all_opinions = faction_table.get_all_opinions()
        assert all_opinions['The Crows']['The Billhooks'] == -1
        assert all_opinions['The Billhooks']['The Crows'] == 0  # Should be unaffected
