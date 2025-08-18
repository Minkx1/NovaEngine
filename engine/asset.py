"""    ===== asset.py =====    """

import pygame

class Asset():
    def __init__(self, engine, img_path, Width = None, Height = None, solid = False):
        self.engine = engine
        self.surface = self.engine.screen
        self.solid = solid

        self.img = pygame.image.load(img_path).convert_alpha()
        if not Width:
            Width = self.img.get_width()
        if not Height:
            Height = self.img.get_height()
        
        self.img = pygame.transform.scale(self.img, (Width, Height))
        self.rect = self.img.get_rect()
     
    
    def draw(self):
        self.surface.blit(self.img, self.rect)
        return self
    
    def set_position(self, x, y):
        self.x, self.y = x, y
        self._update_rect()
        return self

    def place_centered(self, x, y):
        self.rect = self.img.get_rect(center=(x, y))
        self.x, self.y = self.rect.topleft
        return self

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self._update_rect()

    def scale(self, W, H):
        self.img = pygame.transform.scale(self.img, (W, H))
        self._update_rect()
        return self

    def rotate(self, angle):
        self.img = pygame.transform.rotate(self.img, angle)
        self._update_rect(center=True)
        return self

    def _update_rect(self, center=False):
        if center:
            self.rect = self.img.get_rect(center=self.rect.center)
            self.x, self.y = self.rect.topleft
        else:
            self.rect.topleft = (self.x, self.y)