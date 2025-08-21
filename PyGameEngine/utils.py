"""    ===== utils.py =====    """

import pygame, threading
from enum import Enum
from typing import Tuple, Union


class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)


def render_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    font: str = "TimesNewRoman",
    size: int = 14,
    color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK,
    center: bool = False
):
    """
    Render text on the screen at (x, y).

    Args:
        screen: pygame.Surface to draw on
        text: string to render
        x, y: coordinates
        font: font name
        size: font size
        color: text color (Colors enum or RGB tuple)
        center: if True, center the text at (x, y)
    """
    if isinstance(color, Colors):
        color = color.value

    font_obj = pygame.font.SysFont(font, size)
    text_surf = font_obj.render(text, True, color)

    rect = text_surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(text_surf, rect)


def fill_background(
    engine,
    color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK,
    image: pygame.Surface = None
):
    """
    Fill the background with a color or an image.

    Args:
        engine: PyGameEngine instance
        color: background color
        image: optional pygame.Surface to use as background
    """
    screen = engine.screen
    if image:
        screen.blit(image, (0, 0))
    else:
        if isinstance(color, Colors):
            color = color.value
        screen.fill(color)

def thread():
    def decorator(func):
        threading.Thread(target=func, daemon=True).start()
        return func
    return decorator
