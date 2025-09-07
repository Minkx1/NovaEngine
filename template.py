import pygame, novaengine as nova

SCREEN_W, SCREEN_H = 900, 600

Engine = nova.NovaEngine(window_size=(SCREEN_W, SCREEN_H))

Main = nova.Scene()
Menu = nova.Scene()

# Initializing sprites in Main and Menu scenes
with Main.sprites():
    pass

with Menu.sprites():
    pass

Engine.run(Main) # Menu is the first scene to see.