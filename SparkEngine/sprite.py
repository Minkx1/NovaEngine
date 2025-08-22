""" ===== sprite.py ===== """

import pygame

class Sprite:
    """
    Helper class for working with sprites:
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

        # Load original image (keep for transformations)
        self.original_img = pygame.image.load(img_path).convert_alpha()
        self.width = width or self.original_img.get_width()
        self.height = height or self.original_img.get_height()

        # Current image (may be transformed)
        self.img = pygame.transform.scale(self.original_img, (self.width, self.height))
        self.original_img = self.img
        self.rect = self.img.get_rect()
        self.x, self.y = self.rect.topleft

    def draw(self):
        """Draw sprite to the screen surface."""
        if self.alive:
            self.surface.blit(self.img, self.rect)
        return self

    def set_update(self):
        """Decorator to set custom update logic for the sprite."""
        def decorator(func):
            self.update_func = func
            return func
        return decorator

    def set_position(self, x, y):
        """Set top-left position of the sprite."""
        self.rect.topleft = (x, y)
        self.x, self.y = x, y
        return self

    def place_centered(self, x, y):
        """Center the sprite at the given coordinates."""
        self.rect.center = (x, y)
        self.x, self.y = self.rect.topleft
        return self

    def move(self, dx=0, dy=0):
        """Move sprite by (dx, dy)."""
        self.rect.move_ip(dx, dy)
        self.x, self.y = self.rect.topleft
        return self

    def scale(self, width, height):
        """Scale sprite to (width, height), keeping it centered."""
        self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(center=self.rect.center)
        self.x, self.y = self.rect.topleft
        return self

    def rotate(self, angle):
        """Rotate sprite around its center."""
        self.img = pygame.transform.rotate(self.original_img, -angle)
        self.rect = self.img.get_rect(center=self.rect.center)
        self.x, self.y = self.rect.topleft
        return self

    def collide(self, other):
        """Check collision with another sprite."""
        return self.rect.colliderect(other.rect)

    def rect_update(self):
        """Update the rect based on the current image size."""
        self.rect = self.img.get_rect(topleft=self.rect.topleft)
        self.x, self.y = self.rect.topleft
        return self.rect

    def kill(self):
        """Mark sprite as dead (not drawn or updated)."""
        self.alive = False
        return self

    def update(self):
        """Call custom update function or draw by default."""
        if self.update_func:
            self.update_func()
        else:
            self.draw()


class Group:
    """
    Container for managing multiple Sprite objects.
    Provides batch operations like draw, update, add, remove, collisions.
    """

    def __init__(self, *sprites):
        self.sprites = list(sprites)

    def add(self, *sprites):
        for sprite in sprites:
            if sprite not in self.sprites:
                self.sprites.append(sprite)
        return self

    def remove(self, *sprites):
        for sprite in sprites:
            if sprite in self.sprites:
                self.sprites.remove(sprite)
        return self

    def draw(self):
        for sprite in self.sprites:
            sprite.draw()
        return self

    def update(self):
        for sprite in self.sprites:
            sprite.update()
        return self

    def move(self, dx=0, dy=0):
        for sprite in self.sprites:
            sprite.move(dx, dy)
        return self

    def scale(self, width, height):
        for sprite in self.sprites:
            sprite.scale(width, height)
        return self

    def rotate(self, angle):
        for sprite in self.sprites:
            sprite.rotate(angle)
        return self

    def kill(self):
        for sprite in self.sprites:
            sprite.kill()
        return self

    def __iter__(self):
        return iter(self.sprites)

    def __len__(self):
        return len(self.sprites)

    def __getitem__(self, idx):
        return self.sprites[idx]

    def collide(self, sprite):
        """Return list of sprites colliding with given sprite."""
        return [s for s in self.sprites if s.collide(sprite)]


class Button(Sprite):
    last_pressed = False

    def __init__(self, engine, img_path, width=None, height=None):
        super().__init__(engine, img_path, width=width, height=height)

    def check(self):
        """Draw button and return True if it was just pressed."""
        self.draw()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        clicked = mouse_pressed and self.rect.collidepoint(mouse_pos) and not Button.last_pressed
        Button.last_pressed = mouse_pressed
        return clicked