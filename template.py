""" ===== template.py ===== """

import pygame, math
import PyGameEngine as pge

from bullet import Bullet

""" --- 1. Initialize PyGameEngine --- """

# variables and others
SCREEN_W, SCREEN_H = 900, 600 
PLAYER_SPEED = 5
bullet = None

Engine = pge.PyGameEngine().init(window_size=(900, 600))

""" --- 2. Create Scene, Add assets and Initialize function --- """

# Scene1
Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    player = pge.Sprite(
        engine=Engine,img_path="assets/player.png",
        width=120, height=103
    ).place_centered(SCREEN_W/2, SCREEN_H/2)

@Scene1.init_scene()
def scene1():
    pge.fill_background(engine=Engine, color=pge.Colors.WHITE)
        
    #Moving player
    @player.set_update()
    def _():
        global bullet

        pge.ZombieKillerMovement().update(Engine, Scene1.solids, player)     

        if pge.MouseClicked(): 
            bullet = Bullet(Engine, 'assets/bullet.png', 
                            player.rect.center[0], player.rect.center[1], 
                            8,8)

        if bullet: bullet.update()

        player.draw()

    Scene1.update()

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())
