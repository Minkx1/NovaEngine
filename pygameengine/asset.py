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

        
        if self.solid and self.engine:
            if not hasattr(self.engine, "solid_assets"):
                self.engine.solid_assets = []
            self.engine.solid_assets.append(self)
    
    def draw(self):
        self.surface.blit(self.img, self.rect)
        return self
    
    def set_position(self, x, y):
        self.x, self.y = x, y
        self.rect.topleft = (x, y)
        return self

    def place_centered(self, x, y):
        self.rect = self.img.get_rect(center=(x, y))
        return self

    def move(self, dx, dy):
        self.x += dx 
        self.y += dy
        self.rect.topleft = (self.x, self.y) 

    def scale(self, W, H):
        self.img = pygame.transform.scale(self.img, (W, H))

    def rotate(self, angle):
        self.img = pygame.transform.rotate(self.img, angle)
        self.rect = self.img.get_rect(center=self.rect.center)