"""    ===== template.py =====    """

import pygame
import pygameengine as pge

Engine = pge.PyGameEngine()
Engine.init(app_name="PGE test") 

scene_mode = 1

with Engine.assets("Scene1"):
    player1 = pge.Player(
        engine=Engine,
        img_path='img.png',
        x=200, y=200,
        width=50, height=50,
        movement_type="platformer"
    ).place_centered(250, 250)

    ground1 = pge.Asset(
        engine=Engine,
        img_path='img.png',
        Width=500, Height=50,
        solid=True
    ).place_centered(250, 485)

with Engine.assets("Scene2"):
    player2 = pge.Player(
        engine=Engine,
        img_path='img.png',
        x=200, y=200,
        width=50, height=50,
        movement_type="platformer"
    ).place_centered(250, 120)

    ground2 = pge.Asset(
        engine=Engine,
        img_path='img.png',
        Width=500, Height=50,
        solid=True
    ).place_centered(250, 385)

@Engine.scene("Scene1")
def scene1():
    global scene_mode
    Engine.screen.fill(pge.BLACK)

    ground1.draw()
    player1.update()
    if Engine.KeyPressed(pygame.K_2): scene_mode = 2

@Engine.scene("Scene2")
def scene2():
    global scene_mode
    Engine.screen.fill(pge.WHITE)

    ground2.draw()
    player2.update()

    if Engine.KeyPressed(pygame.K_1): scene_mode = 1

run = True
while run:
    run = Engine.run()

    # --- your game cod is here ---
    if scene_mode == 1:
        Engine.run_scene('Scene1')
    elif scene_mode == 2:
        Engine.run_scene('Scene2')
