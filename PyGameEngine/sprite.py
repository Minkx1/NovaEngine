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

        self.update_func = None

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
        self.original_update = None
        self.rect = self.img.get_rect()

        self.x = self.rect.x
        self.y = self.rect.y

    def draw(self):
        """Draw sprite to the screen surface."""
        if self.alive:
            self.surface.blit(self.img, self.rect)
        return self
    
    def set_update(self):
        """Set logic of self.update method."""
        def decorator(func):
            self.update_func = func
            return func
        return decorator

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
        self.img = pygame.transform.rotate(self.original_img, -angle)
        self.rect = self.img.get_rect(center=self.rect.center)
        return self

    def collide(self, Sprite):
        res = False
        if self.rect.colliderect(Sprite.rect): res = True
        return res 

    def rect_update(self):
        self.rect = self.img.get_rect()

        self.x = self.rect.x
        self.y = self.rect.y
        return self.rect

    def kill(self):
        self.alive = False
        return self
    
    def update(self):
        if not self.update_func:
            return self.draw()
        else: 
            self.update_func()


class Group:
    """
    Container for managing multiple Sprite objects.
    Provides batch operations like draw, update, add, remove, collisions.
    """

    def __init__(self, *sprites):
        self.sprites = list(sprites)

    def add(self, *sprites):
        """Add one or more sprites to the group."""
        for sprite in sprites:
            if sprite not in self.sprites:
                self.sprites.append(sprite)
        return self

    def remove(self, *sprites):
        """Remove one or more sprites from the group."""
        for sprite in sprites:
            if sprite in self.sprites:
                self.sprites.remove(sprite)
        return self

    def draw(self):
        """Draw all alive sprites in the group."""
        for sprite in self.sprites:
            sprite.draw()
        return self

    def update(self):
        """Updates all alive sprites in the group."""
        for sprite in self.sprites:
            sprite.update()
        return self

    def move(self, dx=0, dy=0):
        """Move all sprites in the group."""
        for sprite in self.sprites:
            sprite.move(dx, dy)
        return self

    def scale(self, width, height):
        """Scale all sprites in the group."""
        for sprite in self.sprites:
            sprite.scale(width, height)
        return self

    def rotate(self, angle):
        """Rotate all sprites in the group."""
        for sprite in self.sprites:
            sprite.rotate(angle)
        return self

    def kill(self):
        """Kill all sprites in the group."""
        for sprite in self.sprites:
            sprite.kill()
        return self

    def __iter__(self):
        """Iterate over sprites."""
        return iter(self.sprites)

    def __len__(self):
        return len(self.sprites)

    def __getitem__(self, idx):
        return self.sprites[idx]

    def collide(self, sprite):
        """Return list of sprites colliding with given sprite."""
        l = []
        for s in self.sprites:
            if s.collide(sprite):
                l.append(s)
        return l

class Button(Sprite):
    last_pressed = False
    
    def __init__(self, engine, img_path,width=None, height=None):
        super().__init__(engine, img_path, width=width, height=height)
    
    def check(self):
        """Draws button and returns True if pressed"""
        self.draw()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # ліва кнопка

        self.surface.blit(self.img, self.rect)

        clicked = False
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not Button.last_pressed:
                clicked = True

        Button.last_pressed = mouse_pressed
        return clicked