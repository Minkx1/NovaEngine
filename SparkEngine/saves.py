""" ===== saves.py ===== """

import json, os
from pathlib import Path

class SaveManager:
    def __init__(self, engine, appdata=True):
        self.engine = engine
        main_dir = self.engine.app_name

        if appdata:
            if os.name == "nt":  # Windows
                app_data_path = os.getenv("APPDATA")
                self.main_dir = os.path.join(app_data_path, main_dir)
            else:  # Linux/MacOS
                self.main_dir = os.path.join(Path.home(), f".{main_dir}")
        
        os.makedirs(self.main_dir, exist_ok=True)
        self.DATA = os.path.join(self.main_dir, "data.json")

        self.vars = []

    def _get_globals(self):
        """Getting globals()"""
        import inspect
        caller_frame = inspect.currentframe().f_back.f_back
        return caller_frame.f_globals
    
    def set_vars(self, vars: list[str]):
        self.vars = vars

    def save(self):
        """
        Save attributes, e.g.:
        save(["player.hp", "player.money"])
        -> {"player.hp": 100, "player.money": 250}
        """
        g = self._get_globals()
        values = {}

        for key in self.vars:
            parts = key.split(".")
            obj = g.get(parts[0])
            if obj is None:
                continue

            # checking attributes
            for attr in parts[1:]:
                obj = getattr(obj, attr)
            values[key] = obj

        with open(self.DATA, "w", encoding="utf-8") as f:
            json.dump(values, f, indent=4)

        return values

    def load(self):
        """
        Loads data from file and puts them into vars.
        E.G.:
        load(["player.hp", "player.money"])
        -> player.hp and player.money change.
        """
        if not os.path.exists(self.DATA):
            return {}

        with open(self.DATA, "r", encoding="utf-8") as f:
            values = json.load(f)

        g = self._get_globals()
        for key in self.vars:
            if key not in values:
                continue

            parts = key.split(".")
            obj = g.get(parts[0])
            if obj is None:
                continue

            for attr in parts[1:-1]:
                obj = getattr(obj, attr)

            setattr(obj, parts[-1], values[key])

        return values