""" ===== template.py ===== """

import pygame
import NovaEngine as nova

""" --- 1. Initialize PyGameEngine and others --- """

SCREEN_W, SCREEN_H = 900, 600 

Engine = nova.NovaEngine(window_size=(SCREEN_W, SCREEN_H))

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = nova.Scene(Engine) 
Scene2 = nova.Scene(Engine) # if you want to have some more scenes

with Scene1.sprites(): # initilizes all sprites you wanna see in one specific scene. Also if not specified, main function just updates all scene's sprites
    player = nova.Sprite(Engine, "assets/player.png", 100, 100) #creating player
    player.place_centered(SCREEN_W/2, SCREEN_H/2) # placing player center in coordinates
    
    @player.set_update() # what will be happening when called player.update()
    def player_update(): # function to be called - can be named absolutelly as you wish
        
        player.draw() # MUST be in almost every .update()
        player.look_at(pygame.mouse.get_pos()) # makes sprite look at target, that can be point (x, y) or other Sprite object.
        if Engine.MouseClicked(): 
            # When mouse is clicked - moves player in direction he is looking with speed 50.
            player.move_angle(50) 

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run() # input scene you wanna see first, if not inputed - you will see first scene that you have initialized
