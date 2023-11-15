from blades_util.relationshipTable import RelationshipTable

from blades_util.relationshipTable import opinionIndexer, getOpinionModifier


class TestRelationshipTable:
    def test_opinionIndexer(self):
        # Test values within the range
        assert opinionIndexer(1.5) == 1
        assert opinionIndexer(-1.5) == -1
        assert opinionIndexer(0) == 0

        # Test values outside the range
        assert opinionIndexer(4) == 3
        assert opinionIndexer(-4) == -3
        assert opinionIndexer(3.5) == 3
        assert opinionIndexer(-3.5) == -3

        # Test integer values
        assert opinionIndexer(2) == 2
        assert opinionIndexer(-2) == -2

    def test_getOpinionModifier(self):
        # Test values that map directly to the OPINION_MODIFIERS keys
        assert getOpinionModifier(-3) == -0.75
        assert getOpinionModifier(-2) == -0.5
        assert getOpinionModifier(-1) == -0.25
        assert getOpinionModifier(0) == 0
        assert getOpinionModifier(1) == 0.25
        assert getOpinionModifier(2) == 0.5
        assert getOpinionModifier(3) == 0.75

        # Test values that need to be indexed first
        assert getOpinionModifier(4) == 0.75
        assert getOpinionModifier(-4) == -0.75
        assert getOpinionModifier(2.5) == 0.5
        assert getOpinionModifier(-2.5) == -0.5
        assert getOpinionModifier(1.1) == 0.25
        assert getOpinionModifier(-1.1) == -0.25
        assert getOpinionModifier(0.1) == 0
        assert getOpinionModifier(-0.1) == -0

    def test_constructor_with_initializer(self):
        keys = ["a", "b", "c"]
        initializer = lambda a, b: 1 if a != b else 0
        table = RelationshipTable(keys, initializer)

        # Assert that the diagonal is 0
        for key in keys:
            assert table.get(key, key) == 0

        # Assert that other values are 1
        for i in keys:
            for j in keys:
                if i != j:
                    assert table.get(i, j) == 1

    def test_constructor_without_initializer(self):
        keys = ["a", "b", "c"]
        table = RelationshipTable(keys)

        # Assert that all values are 0
        for i in keys:
            for j in keys:
                assert table.get(i, j) == 0

    def test_constructor_with_other_table(self):
        keys = ["a", "b", "c"]
        initializer = lambda a, b: 2 if a != b else 0
        original_table = RelationshipTable(keys, initializer)

        copied_table = original_table.clone()

        # Assert that copied values are the same as the original
        for i in keys:
            for j in keys:
                assert copied_table.get(i, j) == original_table.get(i, j)

    def test_update_opinion(self):
        keys = ["A", "B", "C"]
        table = RelationshipTable(keys)

        # Initial state: everyone feels neutral about everyone else
        assert table.get("A", "B") == 0
        assert table.get("A", "C") == 0
        assert table.get("B", "A") == 0
        assert table.get("B", "C") == 0
        assert table.get("C", "A") == 0
        assert table.get("C", "B") == 0

        # A acts positively upon B by an amount of 2
        actingOn, beingActedUpon, amount, diff_results = table.updateOpinion("A", "B", 2)

        # Check the direct effect: A's action should make B feel more positively about A
        assert table.get("B", "A") == 2

        # Check the indirect effects on C due to opinion modifiers
        # Assuming C was neutral about B, the opinion modifier is 0, so C's opinion about A remains unchanged
        assert table.get("C", "A") == 0

        # Validate the returned values from updateOpinion
        assert actingOn == "A"
        assert beingActedUpon == "B"
        assert amount == 2
        assert diff_results["B"]["A"] == 2

        # Let's make C dislike B by setting their relationship value to -3
        table.set("C", "B", -3)

        # Now, if A acts negatively upon B by an amount of -1, C should feel more positively about A
        # because C dislikes B and "the enemy of my enemy is my friend"
        actingOn, beingActedUpon, amount, diff_results = table.updateOpinion("A", "B", -1)

        # Check the direct effect: A's action should make B feel more negatively about A
        assert table.get("B", "A") == 1  # 2 (previous value) - 1

        # Check the indirect effects on C
        # C dislikes B (-3), so the opinion modifier is -0.75. C's opinion about A should increase by 0.75
        assert table.get("C", "A") == 0.75  # 0 (previous value) + (-1 * -0.75)

        # Validate the returned values from updateOpinion
        assert actingOn == "A"
        assert beingActedUpon == "B"
        assert amount == -1
        assert diff_results['B']['A'] == -1
        assert diff_results['C']['A'] == 0.75

    def test_howOthersFeelAboutMe(self):
        keys = ["A", "B", "C"]
        table = RelationshipTable(keys)
        table.set("A", "B", 1)
        table.set("C", "B", -1)

        # B should see that A feels positively about them and C feels negatively
        opinions_about_B = table.howOthersFeelAboutMe("B")
        assert opinions_about_B == {"A": 1, "C": -1}

        # A should see that no one has an opinion about them since we didn't set it
        opinions_about_A = table.howOthersFeelAboutMe("A")
        assert opinions_about_A == {"B": 0, "C": 0}

    def test_howIfeelAboutOthers(self):
        keys = ["A", "B", "C"]
        table = RelationshipTable(keys)
        table.set("B", "A", 1)
        table.set("B", "C", -1)

        # B should feel positively about A and negatively about C
        my_opinions_as_B = table.howIfeelAboutOthers("B")
        assert my_opinions_as_B == {"A": 1, "C": -1}

        # C should feel neutral about everyone since we didn't set their opinions
        my_opinions_as_C = table.howIfeelAboutOthers("C")
        assert my_opinions_as_C == {"A": 0, "B": 0}
