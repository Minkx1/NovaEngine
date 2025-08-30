"""===== saves.py ====="""

import json, os
from pathlib import Path
import inspect

class SaveManager:
    """
    A manager class for saving and loading object attributes to JSON.

    Example usage:
        save_manager = SaveManager(engine)
        save_manager.set_vars(["player.hp", "player.money"])
        save_manager.save()
        save_manager.load()
    """

    def __init__(self, engine, appdata: bool = True, path:str = None, name:str = "data"):
        """
        Initialize SaveManager.

        Args:
            engine: Reference to the game engine (used for app_name).
            appdata (bool): If True, saves data in OS-specific appdata folder.
                            If False, saves in current working directory.
            path (str): If $appdata$ is False, SaveManager will create folder with saves in $path$ directory. 
                  If $appdata$ is True, then in AppData folder will be created $path$.
            name (str): the name of save file.

        """
        self.engine = engine
        self.path = path
        self.name = name

        if self.path is None: 
            self.path = self.engine.app_name

        # Choose directory depending on OS
        if appdata:
            if os.name == "nt":  # Windows
                self.app_data_path = os.getenv("APPDATA")
                self.main_dir = os.path.join(self.app_data_path, path)
            else:  # Linux / macOS
                self.main_dir = os.path.join(Path.home(), f".{self.path}")
        else:
            self.main_dir = self.path

        os.makedirs(self.main_dir, exist_ok=True)
        
        if self.name:
            self.data_file = os.path.join(self.main_dir, f"{name}.novasave")
        else:
            self.data_file = os.path.join(self.main_dir, "data.json")

        self.vars: list[str] = []
    
    def _get_globals(self) -> dict:
        """
        Get the caller's global variables.
        Used to resolve object references like 'player.hp'.

        Returns:
            dict: The global scope of the caller.
        """
        caller_frame = inspect.currentframe().f_back.f_back
        return caller_frame.f_globals

    def set_vars(self, vars: list[str]):
        """
        Set which attributes should be saved/loaded.

        Args:
            vars (list[str]): A list of attribute paths (e.g. ["player.hp", "player.money"])
        """
        self.vars = vars

    def save(self) -> dict:
        """
        Save selected attributes to JSON.

        Example:
            self.vars = ["player.hp", "player.money"]
            -> creates JSON file like:
               {"player.hp": 100, "player.money": 250}

        Returns:
            dict: The dictionary of saved values.
        """
        g = self._get_globals()
        values = {}

        for key in self.vars:
            parts = key.split(".")
            obj = g.get(parts[0])
            if obj is None:
                continue

            # Traverse object attributes
            for attr in parts[1:]:
                obj = getattr(obj, attr, None)
                if obj is None:
                    break
            if obj is not None:
                values[key] = obj

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(values, f, indent=4)

        return values

    def load(self) -> dict:
        """
        Load saved attributes from JSON and apply them to objects.

        Example:
            self.vars = ["player.hp", "player.money"]
            -> modifies player.hp and player.money values in memory.

        Returns:
            dict: The dictionary of loaded values.
        """
        if not os.path.exists(self.data_file):
            return {}

        with open(self.data_file, "r", encoding="utf-8") as f:
            values = json.load(f)

        g = self._get_globals()
        for key in self.vars:
            if key not in values:
                continue

            parts = key.split(".")
            obj = g.get(parts[0])
            if obj is None:
                continue

            # Traverse until the second-to-last attribute
            for attr in parts[1:-1]:
                obj = getattr(obj, attr, None)
                if obj is None:
                    break

            if obj is not None:
                setattr(obj, parts[-1], values[key])

        return values