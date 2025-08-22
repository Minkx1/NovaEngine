""" ===== main.py ===== """

import pygame
import SparkEngine as SE

""" --- 1. Initialize PyGameEngine and others --- """

SCREEN_W, SCREEN_H = 900, 600 

Engine = SE.SparkEngine(window_size=(SCREEN_W, SCREEN_H))

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = SE.Scene(Engine)

with Scene1.sprites():
    
    pass 

@Scene1.init_scene()
def scene1():
    SE.fill_background(engine=Engine, color=SE.Colors.WHITE)

    # <-- put here some logic

    Scene1.update()

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())
