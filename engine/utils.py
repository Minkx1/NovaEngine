"""    ===== utils.py =====    """

import pygame

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

def render_text(screen, text, x, y, font="TimesNewRoman", size=14, color=Colors.BLACK):
    font_obj = pygame.font.SysFont(font, size)
    text_surf = font_obj.render(text, True, color)
    screen.blit(text_surf, (x, y))

def FillBackground(engine, color = Colors.BLACK):
    screen = engine.screen
    screen.fill(color)