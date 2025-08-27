import pygame
from .sprite import Sprite
from .engine import log

class Button(Sprite):
    def __init__(self, engine, img_path, width=None, height=None):
        super().__init__(engine, img_path, width=width, height=height)

    def check(self):
        """Draw button and return True if it was just pressed."""
        self.draw()

        clicked = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            clicked = self.engine.MouseClicked()

        return clicked


class ProgressBar(Sprite):
    def __init__(
        self,
        engine,
        width,
        height,
        max_value=100,
        value=0,
        bg_color=(50, 50, 50),
        fg_color=(0, 200, 0),
        border_color=(0, 0, 0),
        border_width=2,
    ):
        """
        Клас прогрес-бара
        :param engine: посилання на движок
        :param x, y: позиція
        :param width, height: розміри
        :param max_value: максимальне значення
        :param value: початкове значення
        :param bg_color: колір фону
        :param fg_color: колір прогресу
        :param border_color: колір рамки
        :param border_width: товщина рамки
        """
        super().__init__(engine, None, width, height)

        self.max_value = max_value
        self.value = value

        self.bg_color = bg_color
        self.fg_color = fg_color
        self.border_color = border_color
        self.border_width = border_width

    def set_value(self, value):
        """Встановити значення прогрес-бара"""
        self.value = max(0, min(self.max_value, value))

    def add_value(self, delta):
        """Додати/відняти значення"""
        self.set_value(self.value + delta)

    def draw(self):
        """Draws progress-bar on the screen"""
        if self.alive:
            # bg
            pygame.draw.rect(self.surface, self.bg_color, self.rect)
            # filled
            fill_w = int((self.value / self.max_value) * self.width)
            pygame.draw.rect(
                self.surface,
                self.fg_color,
                (self.rect.x, self.rect.y, fill_w, self.height),
            )
            # Border
            if self.border_width > 0:
                pygame.draw.rect(
                    self.surface,
                    self.border_color,
                    (self.rect.x, self.rect.y, self.width, self.height),
                    self.border_width,
                )

            self.engine.render_text(
                f"{self.value} / {self.max_value}",
                self.rect.centerx,
                self.rect.centery,
                center=True,
            )


class Projectile(Sprite):
    def __init__(self, engine, img_path, width=None, height=None, start = None, target = None, speed:int = 100):
        super().__init__(engine, img_path, width, height)
        self.start = start
        self.target = target
        self.speed = speed
        
        try:
            sx, sy = start[0],start[1] 
            self.place_centered(sx, sy)
        except Exception as e:
            log(e, error=True)

        try:
            self.look_at(pygame.mouse.get_pos())
        except Exception as e:
            log(e, error=True)
    
    def update(self):
        if not self.collide(rect=self.engine.screen.get_rect()): 
            self.kill()
        self.draw()
        self.move_angle(50)