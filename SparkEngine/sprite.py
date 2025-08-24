"""===== sprite.py ====="""

import pygame, random, math


class Sprite:
    """
    Helper class for working with sprites:
    - load image
    - scaling, moving, rotating
    - drawing on the screen
    - animation handling
    """

    def __init__(self, engine, img_path, width=None, height=None, solid=False):
        self.engine = engine
        self.surface = self.engine.screen
        self.solid = solid
        self.alive = True

        self.update_func = None

        self.debug_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.debug = engine.debug

        # Load original image (keep for transformations)
        if img_path:
            self.original_img = pygame.image.load(img_path).convert_alpha()
        else:
            self.original_img = pygame.Surface((0, 0))
        self.width = width or self.original_img.get_width()
        self.height = height or self.original_img.get_height()

        # Current image (may be transformed)
        self.img = pygame.transform.scale(self.original_img, (self.width, self.height))
        self.original_img = self.img
        self.angle: float = 0
        self.rect = self.img.get_rect()
        self.x, self.y = self.rect.topleft

        # animations
        self.animations = {}
        self.current_animation: str = None

    def draw(self):
        """Draw sprite to the screen surface."""
        if self.alive:
            rotated_img = pygame.transform.rotate(self.img, self.angle)
            rotated_rect = rotated_img.get_rect(center=self.rect.center)
            self.surface.blit(rotated_img, rotated_rect.topleft)
        if self.debug:
            pygame.draw.rect(self.surface, self.debug_color, self.rect, 1)
            self.engine.render_text(
                f"{round(self.rect.x)}, {round(self.rect.y)}",
                self.rect.x,
                self.rect.y,
                size=12,
                center=True,
            )
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

    def move_to(self, target, speed: float):
        """
        Move sprite towards a target (Sprite or (x, y)) with given speed.

        Args:
            target (Sprite | tuple): Target point or another sprite.
            speed (float): Movement speed (pixels per frame, scaled by dt).
        """
        # getting target.x and target.y
        if isinstance(target, Sprite):
            tx, ty = target.rect.center
        else:
            tx, ty = target

        dx, dy = tx - self.rect.centerx, ty - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > 0:
            # нnormalize
            dx /= dist
            dy /= dist

            # moveing sprite
            self.rect.x += dx * speed * self.engine.dt
            self.rect.y += dy * speed * self.engine.dt

    def scale(self, width, height):
        """Scale sprite to (width, height), keeping it centered."""
        self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(center=self.rect.center)
        self.x, self.y = self.rect.topleft
        return self

    def rotate(self, angle):
        """Rotate sprite around its center."""
        self.angle = (self.angle + angle) % 360
        return self

    def look_at(self, target):
        if isinstance(target, Sprite):
            tx, ty = target.rect.center
        else:
            tx, ty = target
        dx, dy = tx - self.rect.centerx, ty - self.rect.centery
        self.angle = -math.degrees(math.atan2(dy, dx))

    def collide(self, other=None, rect=None):
        """Check collision with another sprite."""
        ans = False
        if other and other.alive:
            ans = self.rect.colliderect(other.rect)
        elif rect:
            ans = self.rect.colliderect(rect)
        return ans

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
        if self.alive:
            if self.update_func:
                self.update_func()
            else:
                self.draw()

    # ====== ANIMATIONS ======
    def set_animation(self, name, frames, speed=0.1, loop=True):
        """
        Register a new animation for the sprite.
        """
        self.animations[name] = {
            "frames": frames,
            "index": 0,
            "speed": speed,
            "timer": 0,
            "loop": loop,
        }

        # одразу ставимо цю анімацію активною, якщо ще немає
        if not self.current_animation:
            self.current_animation = name
            self.img = frames[0]
            self.rect_update()
        return self

    def play_animation(self, name=None):
        """
        Play/update animation each frame.
        If name is passed, switch to that animation.
        """
        if not self.animations:
            return

        # Перемикання на іншу анімацію
        if name and name != self.current_animation:
            self.current_animation = name
            self.animations[name]["index"] = 0
            self.animations[name]["timer"] = 0
            self.img = self.animations[name]["frames"][0]
            self.rect_update()
            return

        anim = self.animations[self.current_animation]
        dt = self.engine.dt

        anim["timer"] += dt
        if anim["timer"] >= anim["speed"]:
            anim["timer"] = 0
            anim["index"] += 1

            if anim["index"] >= len(anim["frames"]):
                if anim["loop"]:
                    anim["index"] = 0
                else:
                    anim["index"] = len(anim["frames"]) - 1

            self.img = anim["frames"][anim["index"]]
            self.rect_update()

    @staticmethod
    def CreateImage(path="", width: int = None, height: int = None):
        img = pygame.image.load(path).convert_alpha()
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img


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
