import pygame, math
from PyGameEngine import Sprite

class Bullet(Sprite):
    def __init__(
            self, 
            engine, 
            img_path : str,
            x: float, y: float, 
            width: float = None, height:float = None,
            speed: int = 100):
        super().__init__(engine, img_path, width, height, False)

        self.x, self.y = x, y 
        self.place_centered(x, y)

        self.mouse_pos = pygame.mouse.get_pos()
        dx, dy = self.mouse_pos[0] - x, self.mouse_pos[1] - y
        dist = math.hypot(dx, dy)  # довжина вектора
        if dist == 0: dist = 1

        self.vel_x = dx / dist * speed
        self.vel_y = dy / dist * speed

    def update(self):
        if self.alive:
            self.draw()
            self.move(self.vel_x, self.vel_y)
            if self.x < 0 or self.x > self.engine.screen.get_width():
                if self.y < 0 or self.y > self.engine.screen.get_height():
                    self.kill()