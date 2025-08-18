""" ===== player.py ===== """

from .sprite import Sprite


class Player(Sprite):
    """
    Player class extending Sprite, with movement logic.
    The movement behavior is delegated to a Movement class
    (PlatformerMovement or TopDownMovement).
    """

    def __init__(
        self,
        engine,
        img_path: str,
        x: int,
        y: int,
        width: int = None,
        height: int = None,
        movement_type=None
    ):
        """
        Initialize a player.

        Args:
            engine: PyGameEngine instance
            img_path: path to the player's image
            x, y: initial coordinates
            width, height: optional size
            movement_type: an instance of movement class (PlatformerMovement / TopDownMovement)
        """
        super().__init__(engine, img_path, width, height, solid=False)
        self.set_position(x, y)

        # velocity for movement
        self.vel_x = 0
        self.vel_y = 0

        if not movement_type:
            raise ValueError("Movement type must be specified")
        self.movement_type = movement_type

    def update(self):
        """
        Update player position using the assigned movement_type.
        Draws the player sprite.
        """
        keys = self.engine.keys_pressed

        self.movement_type.update(
            engine=self.engine,
            keys=keys,
            solids=self.solid_assets,
            rect=self.rect
        )
        self.draw()

    @property
    def solid_assets(self):
        """
        Return a list of solid sprites in the current active scene.
        Used for collision detection.
        """
        if self.engine.active_scene is None:
            return []
        return self.engine.active_scene.solids
