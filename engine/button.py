"""    ===== template.py =====    """

import pygame
from .asset import Asset

class Button(Asset):
    last_pressed = False
    
    def __init__(self, engine, x, y, img_path,width=None, height=None):
        super().__init__(engine, img_path, Width=width, Height=height)

        self.set_position(x, y)
    
    def draw(self):
        """Draws button and returns True if pressed"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # ліва кнопка

        self.surface.blit(self.img, self.rect)

        clicked = False
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not Button.last_pressed:
                clicked = True

        Button.last_pressed = mouse_pressed
        return clicked
