from typing import Tuple, Callable


class Model:

    def __init__(self):
        self.update_output: Callable[[list[str]], None] = None
        self.selected_manager = None
        self.managers = []
        self.current_output_list = []
        self.list_updater: Callable[[list[str]], None] = None
        self.current_manager_holder: Callable[[Tuple[str, dict[tuple[str, str], float]]], None] = None
        self.selected_faction = None

    def set_current_manager_holder(self, updater: Callable[[str, dict[tuple[str, str], float]], None]):
        self.current_manager_holder = updater

    def update_current_manager(self, name: str, factions: dict[tuple[str, str], float]) -> None:
        self.current_manager_holder(name, factions)

    def get_selected(self) -> str:
        return self.selected_faction

    def set_selected(self, selected_faction: str):
        self.selected_faction = selected_faction

    def set_manager_list_updater(self, list_updater: Callable[[list[str]], None]):
        self.list_updater = list_updater
        if self.managers:
            self.list_updater(self.managers)

    def update_managers(self, managers: list[str]):
        self.managers = managers
        if self.list_updater:
            self.list_updater(self.managers)

    def set_selected_manager(self, manager: str):
        self.selected_manager = manager

    def set_output_holder(self, update_output: Callable[[list[str]], None]):
        self.update_output = update_output
        self.update_output(self.current_output_list)

    def current_output(self, output: list[str]):
        self.current_output_list = output
        if self.update_output:
            self.update_output(self.current_output_list)
