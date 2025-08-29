"""===== gui.py ====="""

import pygame
from .sprite import Sprite


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


class ToggleButton(Button):
    def __init__(
        self, engine, img_path=[str, str], width=None, height=None, start_state=False
    ):
        super().__init__(engine, img_path, width, height)
        self.state = start_state
        self.img_0, self.img_1 = img_path[0], img_path[0]

    def draw(self):
        if not self.state:
            self.img = self.img_0
        else:
            self.img = self.img_1

        super().draw()
        return self

    def master_check(self):
        """Returns True if it was just pressed."""

        clicked = False
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            clicked = self.engine.MouseClicked()

        return clicked

    def check(self):
        clicked = self.master_check()
        if clicked:
            self.state = not self.state
        return self.state


class TextLabel(Sprite):
    def __init__(
        self,
        engine,
        x,
        y,
        text="",
        font="TimesNewRoman",
        size=16,
        color=(0, 0, 0),
        center=False,
    ):
        super().__init__(engine, None)
        self.x = x
        self.y = y
        self.text = text
        self.render_text = self.text
        self.font = font
        self.size = size
        self.color = color
        self.center = center

        self.bound_obj = None
        self.bound_attr = None

    def set_text(self, new_text):
        self.text = new_text

    def bind(self, var: str):
        from .engine import get_globals

        GLOBALS = get_globals()

        parts = var.split(".")
        obj_name = parts[0]
        attr_name = parts[1]

        obj = GLOBALS.get(obj_name)
        if obj is None:
            raise ValueError(f"Object '{obj_name}' not found in main globals")

        self.bound_obj = obj
        self.bound_attr = attr_name
        return self

    def draw(self):
        self.engine.render_text(
            self.render_text,
            self.x,
            self.y,
            self.font,
            self.size,
            self.color,
            self.center,
        )

    def update(self):
        # if bound
        if self.bound_obj and self.bound_attr:
            self.render_text = self.text + str(getattr(self.bound_obj, self.bound_attr))
        self.draw()


class TextInput(Sprite):
    """Поле для введення тексту, як в Tkinter Entry."""

    def __init__(
        self,
        engine,
        x,
        y,
        width=200,
        height=30,
        font="TimesNewRoman",
        size=16,
        color=(0, 0, 0),
        bg_color=(255, 255, 255),
    ):
        super().__init__(engine, None, width, height)
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.color = color
        self.bg_color = bg_color
        self.value = ""
        self.active = True
        self.current_input = ""

        self.engine.event_handlers.append(self)

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_RETURN:
                self.value = self.current_input
                self.current_input = ""
            else:
                self.current_input += event.unicode

    def draw(self):
        # фон
        pygame.draw.rect(
            self.surface, self.bg_color, (self.x, self.y, self.width, self.height)
        )
        # текст
        text_rect = self.engine.render_text(
            self.current_input,
            self.x + 5,
            self.y + self.height // 2,
            self.font,
            self.size,
            self.color,
        )
        return text_rect

    def update(self):
        self.draw()


class CheckBox(Sprite):
    def __init__(
        self,
        engine,
        x,
        y,
        width=20,
        height=20,
        text="",
        font="TimesNewRoman",
        size=16,
        color=(0, 0, 0),
        state=False,
    ):
        super().__init__(engine, None, width, height)
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y
        self.text = text
        self.font, self.size, self.color = font, size, color
        self.state = state

    def check(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.engine.MouseClicked():
                self.state = not self.state
        return self.state

    def draw(self):
        pygame.draw.rect(self.surface, (0, 0, 0), self.rect, 2)
        if self.state:
            pygame.draw.line(
                self.surface, (0, 0, 0), self.rect.topleft, self.rect.bottomright, 2
            )
            pygame.draw.line(
                self.surface,
                (0, 0, 0),
                (self.x + self.width, self.y),
                (self.x, self.y + self.height),
                2,
            )
        self.engine.render_text(
            self.text, self.x + 30, self.y, self.font, self.size, self.color
        )

    def update(self):
        self.check()
        self.draw()
