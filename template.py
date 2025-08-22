""" ===== template.py ===== """

import pygame, math, threading
import PyGameEngine as pge

from bullet import Bullet

""" --- 1. Initialize PyGameEngine --- """

# variables and others
SCREEN_W, SCREEN_H = 900, 600 
PLAYER_SPEED = 5
magazine_size = 10

Engine = pge.PyGameEngine(window_size=(900, 600))
Engine.show_fps = True

""" --- 2. Create Scene, Add assets and Initialize function --- """

# Scene1
Scene1 = pge.Scene(Engine)

with Scene1.init():
    player = pge.Sprite(
        engine=Engine,img_path="assets/player.png",
        width=120, height=103
    ).place_centered(SCREEN_W/2, SCREEN_H/2)
    player.magazine = magazine_size
    
    bullets = pge.Group()

    @player.set_update()
    def _():
        global bullets

        player.draw()
        pge.ZombieKillerMovement().update(Engine, Scene1.solids, player)        

        if Engine.MouseClicked() and player.magazine > 0: 
            bullets.add(Bullet(Engine, 'assets/bullet.png',player.rect.center[0], player.rect.center[1],8,8))
            player.magazine -= 1 

        if Engine.KeyPressed(pygame.K_r):
            @Engine.Timer(1)
            def _():
                player.magazine = magazine_size

        for bullet in bullets: 
            if not bullet.alive: bullets.remove(bullet)   

@Scene1.logic()
def scene1():
    Engine.fill_background(pge.Colors.WHITE)

    Scene1.update()
    
    Engine.render_text(f"Round: {player.magazine}", SCREEN_W-70, SCREEN_H-20, size=30, color=pge.Colors.RED, center=True)

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())
