"""    ===== player.py =====    """
import pygame
from .asset import Asset

class Player(Asset):
    def __init__(self, engine, img_path, x, y, width=None, height=None, movement_type="platformer"):
        super().__init__(engine, img_path, width, height)
        self.engine = engine  
        self.solid_assets = engine.solid_assets
        self.set_position(x, y)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.movement_type = movement_type.lower()
        self.gravity = 0.8
        self.jump_force = -12
        self.on_ground = False

    def update(self):
        keys = self.engine.keys_pressed  # беремо ключі прямо з Engine
        if self.movement_type == "platformer":
            self._platformer_update(keys)
        elif self.movement_type == "4dir":
            self._fourdir_update(keys)
        
        self._stay_in_bounds()
        self.draw()

    def _platformer_update(self, keys):
        # Walking right-left
        self.vel_x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = self.speed

        # стрибок (тільки якщо на землі)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel_y = self.jump_force
            self.on_ground = False

        # гравітація
        self.vel_y += self.gravity

        # оновлення позиції
        # рух по X
        self.rect.x += self.vel_x
        for asset in getattr(self, 'solid_assets', []):
            if asset.solid and self.rect.colliderect(asset.rect):
                if self.vel_x > 0:
                    self.rect.right = asset.rect.left
                elif self.vel_x < 0:
                    self.rect.left = asset.rect.right
        
        # рух по Y
        self.rect.y += self.vel_y
        self.on_ground = False
        for asset in getattr(self, 'solid_assets', []):
            if asset.solid and self.rect.colliderect(asset.rect):
                # якщо падаємо вниз - стаємо на платформу
                if self.vel_y > 0:
                    self.rect.bottom = asset.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # якщо стрибаємо вгору - не пролізти крізь платформу
                elif self.vel_y < 0:
                    self.rect.top = asset.rect.bottom
                    self.vel_y = 0     

    def _fourdir_update(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed

        self.rect.x += dx
        for asset in getattr(self, 'solid_assets', []):
            if asset.solid and self.rect.colliderect(asset.rect):
                if dx > 0:
                    self.rect.right = asset.rect.left
                elif dx < 0:
                    self.rect.left = asset.rect.right

        self.rect.y += dy
        for asset in getattr(self, 'solid_assets', []):
            if asset.solid and self.rect.colliderect(asset.rect):
                if dy > 0:
                    self.rect.bottom = asset.rect.top
                elif dy < 0:
                    self.rect.top = asset.rect.bottom

    def _stay_in_bounds(self):
        screen_w, screen_h = self.engine.screen.get_size()

        if self.movement_type == "platformer":
            # Обмеження зліва, справа і зверху
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_w:
                self.rect.right = screen_w
            if self.rect.top < 0:
                self.rect.top = 0
            # падіння вниз не обмежуємо
        elif self.movement_type == "4dir":
            # Обмеження з усіх сторін
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > screen_w:
                self.rect.right = screen_w
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_h:
                self.rect.bottom = screen_h