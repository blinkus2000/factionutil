import csv
from typing import Callable, Dict, Tuple, List, IO

OPINION_MODIFIERS = {
    -3: -0.75,
    -2: -0.5,
    -1: -0.25,
    0: 0,
    1: 0.25,
    2: 0.5,
    3: 0.75
}


def opinionIndexer(opinion: float) -> int:
    return int(max(-3, min(3, opinion)))


def getOpinionModifier(opinion: float) -> float:
    return OPINION_MODIFIERS.get(opinionIndexer(opinion), 0)


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


class RelationshipTable:
    def __init__(self, keys: List[str], initializer: Callable[[str, str], float] = None):
        self.keys = keys
        self.initializer: Callable[[str, str], float] = initializer if initializer else lambda a, b: 0
        self.table: Dict[Tuple[str, str], float] = {}
        self.update_all(self.initializer)

    def update_all(self, initializer: Callable[[str, str], float]) -> None:
        for key_i in self.keys:
            for key_j in self.keys:
                self.table[(key_i, key_j)] = 0.0 if key_i == key_j else initializer(key_i, key_j)

    def get(self, key1: str, key2: str) -> float:
        return self.table.get((key1, key2), 0.0)

    def set(self, key1: str, key2: str, val: float) -> None:
        clamped_val = max(-3, min(val, 3))
        self.table[(key1, key2)] = 0.0 if key1 == key2 else clamped_val

    def clone(self) -> 'RelationshipTable':
        new_table = RelationshipTable(self.keys, self.initializer)
        new_table.table = self.table.copy()
        return new_table

    def updateOpinion(self, actingOn: str, beingActedUpon: str, incomingOpinion: float) -> Tuple[
        str, str, float, Dict[Tuple[str, str], float]]:
        oldTable = self.clone()
        self.actUpon(actingOn, beingActedUpon, incomingOpinion)

        for otherKey in (key for key in self.keys if key != actingOn and key != beingActedUpon):
            otherOpinion = self.get(otherKey, beingActedUpon)
            opinionModifier = getOpinionModifier(otherOpinion)
            adjustedOpinion = incomingOpinion * opinionModifier
            self.actUpon(actingOn, otherKey, adjustedOpinion)

        totalResult = self.diff(oldTable)
        return actingOn, beingActedUpon, incomingOpinion, totalResult

    def diff(self, oldTable: 'RelationshipTable') -> Dict[Tuple[str, str], float]:
        result: Dict[Tuple[str, str], float] = {}
        for key1 in self.keys:
            for key2 in self.keys:
                newVal = self.get(key1, key2)
                oldVal = oldTable.get(key1, key2)
                delta = newVal - oldVal
                if delta != 0:
                    result[(key1, key2)] = delta
        return result

    def actUpon(self, actingOn: str, beingActedUpon: str, amount: float) -> None:
        currentFeelings = self.get(beingActedUpon, actingOn)
        newFeelings = currentFeelings + amount
        self.set(beingActedUpon, actingOn, newFeelings)

    def howOthersFeelAboutMe(self, meKey: str) -> Dict[str, float]:
        opinions_about_me: Dict[str, float] = {}
        for key in self.keys:
            if key != meKey:
                opinions_about_me[key] = self.get(key, meKey)
        return opinions_about_me

    def howIfeelAboutOthers(self, meKey: str) -> Dict[str, float]:
        my_opinions_about_others: Dict[str, float] = {}
        for key in self.keys:
            if key != meKey:
                my_opinions_about_others[key] = self.get(meKey, key)
        return my_opinions_about_others
