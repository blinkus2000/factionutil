# Assuming you have a test JSON file with test factions
from typing import Dict
import os
import pytest


from blades_util.faction import Faction, load_factions, save_factions

JSON_PATH = 'factions.json'
TEST_JSON_PATH = 'test_factions.json'


def cleanup_test_path():
    if os.path.exists(TEST_JSON_PATH):
        os.remove(TEST_JSON_PATH)


class TestFaction:

    @pytest.fixture
    def factions(self):
        return load_factions(JSON_PATH)

    @pytest.fixture(autouse=True)
    def cleanup_before_after(self):
        print(f'cleaning up {TEST_JSON_PATH} if it exists on setup')
        cleanup_test_path()
        yield
        print(f'cleaning up {TEST_JSON_PATH} if it exists on teardown')
        cleanup_test_path()

    def test_rating(self, factions):
        for faction_name, faction in factions.items():
            assert factions.rating_table[faction] == faction.rating()
            faction.set_rating(5)
            assert factions.rating_table[faction] == 5

    def test_action(self, factions):
        for faction_name, faction in factions.items():
            assert factions.action_table[faction] == faction.action()
            faction.set_action(5)
            assert factions.action_table[faction] == 5

    def test_save_factions(self, factions):

        save_factions(TEST_JSON_PATH, factions)
        saved_factions: dict[str, Faction] = load_factions(TEST_JSON_PATH)

        for faction_name, faction in saved_factions.items():
            assert factions[faction_name].rating() == faction.rating()
            assert factions[faction_name].action() == faction.action()
            faction.set_action(27)
            faction.set_rating(27)
            assert factions[faction_name].rating() != faction.rating()
            assert factions[faction_name].action() != faction.action()

        saved_factions = load_factions(TEST_JSON_PATH)

        for faction_name, faction in saved_factions.items():
            assert factions[faction_name].rating() == faction.rating()
            assert factions[faction_name].action() == faction.action()
            faction.set_action(27)
            faction.set_rating(27)
            assert factions[faction_name].rating() != faction.rating()
            assert factions[faction_name].action() != faction.action()
