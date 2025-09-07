import pygame as pg
import NovaEngine as nova

class window:
    def __init__(self, x, y):
        self.x, self.y = (x, y)
        self.size = (self.x, self.y)
        self.rect = (0, 0, self.x, self.y)
SCREEN = window(500, 500)

app = nova.NovaEngine(SCREEN.size, "NovaTest", "assets/icon.png", 60).set_debug(True)

s = nova.Scene()
with s.sprites():
    test_sprite = nova.Sprite("assets/player.png", 75, 75).set_position(100, 100)

@s.function()
def _():

    s.update()

app.run()