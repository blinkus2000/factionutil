import os
import pytest
from blades_util.factionManager import FactionManager
from blades_util.factionTable import FactionTable
from blades_util.persistanceManager import save_to, load_from, get_faction_manager, save_faction_manager
from blades_util.relationshipTable import RelationshipTable

JSON_PATH = 'factions.json'  # do not edit or change this file
TEST_JSON_PATH = 'test_factions.json'
TEST_CSV_FILE = 'test_relationship_table.csv'


def cleanup_test_path():
    if os.path.exists(TEST_JSON_PATH):
        os.remove(TEST_JSON_PATH)
    if os.path.exists(TEST_CSV_FILE):
        os.remove(TEST_CSV_FILE)


class TestPersistence:
    @pytest.fixture(autouse=True)
    def cleanup_before_after(self):
        cleanup_test_path()
        yield
        cleanup_test_path()

    @pytest.fixture
    def faction_table(self):
        # Set up the FactionTable with a path to the test JSON
        table = FactionTable(JSON_PATH)
        table.seed_the_relationship_table()  # randomizes all the relationships
        return table

    @pytest.fixture
    def manager(self, faction_table):
        # Set up the FactionManager with the faction table
        return FactionManager(faction_table)

    def test_save_load_faction_manager(self, manager):
        # Save the current state of the manager to JSON and CSV files
        save_faction_manager(manager, TEST_JSON_PATH, TEST_CSV_FILE)

        # Check that the files were created
        assert os.path.exists(TEST_JSON_PATH)
        assert os.path.exists(TEST_CSV_FILE)

        # Load the saved state and compare with the original
        with open(TEST_CSV_FILE, 'r', newline='', encoding='utf-8') as csv_file:
            loaded_table = load_from(csv_file)
            assert loaded_table == manager.faction_table.relationship_table

        # Use the get_faction_manager function to create a FactionManager
        new_manager = get_faction_manager(JSON_PATH, TEST_CSV_FILE)
        # Check if the manager was created successfully
        assert isinstance(new_manager, FactionManager)
        # Further checks can be added to verify the contents of the manager
        # Further checks can be added to verify the contents of the loaded data
