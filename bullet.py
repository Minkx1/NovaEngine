import pygame, math
from SparkEngine import Sprite

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
        dist = math.hypot(dx, dy)
        if dist == 0: dist = 1

        self.vel_x = dx / dist * speed
        self.vel_y = dy / dist * speed
    
    def move(self, dx, dy):
        super().move(dx, dy)
        self.x,self.y = self.rect.x, self.rect.y

    def update(self):
        if self.alive:
            self.draw()
            self.move(self.vel_x, self.vel_y)
            
            if (self.x + self.width < 0 or self.x > self.engine.screen.get_width()
                or self.y + self.height < 0 or self.y > self.engine.screen.get_height()):
                self.kill()