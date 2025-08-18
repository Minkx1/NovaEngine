"""    ===== scenes.py =====    """

import pygame
from contextlib import contextmanager
from .asset import Asset
from .button import Button
from .player import Player

class Scene():
    def __init__(self, engine):
        self.engine = engine
        self.objects = []
        self.solids = []
        self.run = None

        self.engine.scenes.append(self)
        self.engine.active_scene = self

    def add_assets(self, assets_list=[]):
        for obj in assets_list:
            self.objects.append(obj)
            if obj.solid: 
                self.solids.append(obj)
    
    @contextmanager
    def assets(self):
        # Getting locals before with
        import inspect
        frame = inspect.currentframe().f_back.f_back  
        before_vars = set(frame.f_locals.keys())

        yield

        after_vars = frame.f_locals
        new_vars = set(after_vars.keys()) - before_vars

        for name in new_vars:
            obj = after_vars[name]
            if isinstance(obj, (Button, Asset, Player)):
                self.objects.append(obj)
                if obj.solid:
                    self.solids.append(obj)
    
    def init_scene(self):
        def decorator(func):
            self.run = func
            return func
        return decorator
    
    