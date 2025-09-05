import pygame, NovaEngine as nova

SCREEN_W, SCREEN_H = 900, 600

Engine = nova.NovaEngine(window_size=(SCREEN_W, SCREEN_H))

Main = nova.Scene(Engine)
Menu = nova.Scene(Engine)

# Initializing sprites in Main and Menu scenes
with Main.sprites():
    pass

with Menu.sprites():
    pass

Engine.run(Menu) # Menu is the first scene to see.