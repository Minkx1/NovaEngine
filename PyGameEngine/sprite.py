""" ===== sprite.py ===== """

import pygame

class Sprite:
    """
    A helper class for working with sprites:
    - load image
    - scaling, moving, rotating
    - drawing on the screen
    """

    def __init__(self, engine, img_path, width=None, height=None, solid=False):
        self.engine = engine
        self.surface = self.engine.screen
        self.solid = solid
        self.alive = True

        # Load original image (kept for quality when scaling/rotating)
        self.original_img = pygame.image.load(img_path).convert_alpha()
        self.width, self.height = width, height
        if width is None:
            self.width = self.original_img.get_width()
        if height is None:
            self.height = self.original_img.get_height()

        # Current image (may be transformed)
        self.img = pygame.transform.scale(self.original_img, (self.width, self.height))
        self.original_img = self.img
        self.rect = self.img.get_rect()

    def draw(self):
        """Draw sprite to the screen surface."""
        if self.alive:
            self.surface.blit(self.img, self.rect)
        return self

    def set_position(self, x, y):
        """Set top-left position of the sprite."""
        self.rect.topleft = (x, y)
        return self

    def place_centered(self, x, y):
        """Center the sprite at the given coordinates."""
        self.rect.center = (x, y)
        return self

    def move(self, dx=0, dy=0):
        """Move sprite by (dx, dy)."""
        self.rect.move_ip(dx, dy)  # move in place
        return self

    def scale(self, width, height):
        """Scale sprite to (width, height)."""
        self.img = pygame.transform.scale(self.img, (width, height))
        # Keep sprite centered after rescaling
        self.rect = self.img.get_rect(center=self.rect.center)
        return self

    def rotate(self, angle):
        """Rotate sprite around its center."""
        self.img = pygame.transform.rotate(self.original_img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)
        return self

    def kill(self):
        self.alive = False
        return self
