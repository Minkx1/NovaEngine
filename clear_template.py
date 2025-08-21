""" ===== main.py ===== """

import pygame
import PyGameEngine as pge

""" --- 1. Initialize PyGameEngine and others --- """

SCREEN_W, SCREEN_H = 900, 600 

Engine = pge.PyGameEngine().init(window_size=(SCREEN_W, SCREEN_H))

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    
    pass 

@Scene1.init_scene()
def scene1():
    pge.fill_background(engine=Engine, color=pge.Colors.WHITE)

    # <-- put here some logic, like @sprite1.set_update()

    Scene1.update()

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())
