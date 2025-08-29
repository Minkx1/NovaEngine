import pygame, NovaEngine as nova

SCREEN_W, SCREEN_H = 900, 600

Engine = nova.NovaEngine(window_size=(SCREEN_W, SCREEN_H))

Main = nova.Scene(Engine)
Menu = nova.Scene(Engine)

# Initializing sprites in Main scene
with Main.sprites():
    player = nova.Sprite(Engine, "assets/player.png", 100, 100) #creating player
    player.place_centered(SCREEN_W/2, SCREEN_H/2) # placing player center in coordinates
    
    @player.set_update() # what will be happening when called player.update()
    def player_update(): # function to be called - can be named absolutelly as you wish
        
        player.draw() # MUST be in almost every .update()
        player.look_at(pygame.mouse.get_pos()) # makes sprite look at target, that can be point (x, y) or other Sprite object.
        if Engine.MouseClicked(): 
            # When mouse is clicked - moves player in direction he is looking with speed 50.
            player.move_angle(50) 

with Menu.sprites():
    menu_text = nova.TextLabel(Engine, SCREEN_W/2, SCREEN_H/2-100, "M E N U", size=32, center=True)
    hint = nova.TextLabel(Engine, SCREEN_W/2, SCREEN_H/2, "Press M for game", size=16, center=True)

@Menu.function() #Sets main function for Menu
def _():
    Menu.update() 
    if Engine.KeyPressed(pygame.K_m): Engine.set_active_scene(Main) # if M is pressed, active_scene is set to Main, so Engine will render Main scene.

Engine.run(Menu) # Menu is the first scene to see.