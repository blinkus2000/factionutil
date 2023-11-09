from typing import Tuple, Callable


class Model:

    def __init__(self):
        self.current_manager_holder = None
        self.selected_faction = None

    def set_current_manager_holder(self, updater: Callable[[Tuple[str, dict[tuple[str, str], float]]], None]):
        self.current_manager_holder = updater

    def update_current_manager(self, name: str, factions: dict[tuple[str, str], float]) -> None:
        self.current_manager_holder(name, factions)

    def get_selected(self) -> str:
        return self.selected_faction

    def set_selected(self, selected_faction: str):
        self.selected_faction = selected_faction
