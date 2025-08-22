""" ===== scenes.py ===== """

from contextlib import contextmanager
from .sprite import Sprite, Group


class Scene:
    """
    Scene class for organizing game objects.
    - Holds all sprites, buttons, players, etc.
    - Manages solid objects for collision detection.
    - Provides context manager for automatic sprite registration.
    """

    def __init__(self, engine):
        """
        Initialize a new scene.

        Args:
            engine: SparkEngine instance
        """
        self.engine = engine
        self.objects = []  # all sprites in scene
        self.solids = []   # only solid sprites
        self.run = None    # main update function

        # Register scene in engine
        self.engine.scenes.append(self)
        self.engine.active_scene = self

    # ========================
    # OBJECT MANAGEMENT
    # ========================
    def add_sprite(self, sprites_list=[]):
        """Add sprites to the scene manually."""
        for obj in sprites_list:
            self.objects.append(obj)
            if getattr(obj, "solid", False):
                self.solids.append(obj)

    @contextmanager
    def init(self):
        """
        Context manager to auto-register newly created sprites.
        Usage:
            with scene.sprites():
                sprite1 = Sprite(...)

                @sprite1.set_update()
                def _(): ...
        """
        import inspect
        frame = inspect.currentframe().f_back.f_back
        before_vars = set(frame.f_locals.keys())

        yield  # user creates sprites inside this block

        after_vars = frame.f_locals
        new_vars = set(after_vars.keys()) - before_vars

        for name in new_vars:
            obj = after_vars[name]
            if isinstance(obj, (Sprite, Group)):
                self.objects.append(obj)
                if getattr(obj, "solid", False):
                    self.solids.append(obj)

    # ========================
    # SCENE LOOP
    # ========================
    def logic(self):
        """Decorator to register the main update function for the scene."""
        def decorator(func):
            self.run = func
            return func
        return decorator

    def update(self):
        """Call update() on all scene objects."""
        for obj in self.objects:
            obj.update()
