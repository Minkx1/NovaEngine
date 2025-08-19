""" ===== template.py ===== """

import pygame, math
import PyGameEngine as pge

from bullet import Bullet

""" --- 1. Initialize PyGameEngine --- """

SCREEN_W, SCREEN_H = 900, 600 

Engine = pge.PyGameEngine()
Engine.init(
    window_size=(900, 600)
)

bullet = None

""" --- 2. Create Scene, Add assets and Initialize function --- """

Main = pge.Scene(Engine)

with Main.sprites():
    player = pge.Player(
        engine=Engine,
        img_path="assets/player.png",
        x=450, y=100,
        width=120, height=103,
        movement_type=pge.TopDownMovement()
    ).place_centered(SCREEN_W/2, SCREEN_H/2)

@Main.init_scene()
def main_scene():
    global bullet
    pge.fill_background(engine=Engine, color=(225, 225, 225))

    player.update()

    mouse_x,mouse_y = pygame.mouse.get_pos()
    px,py = player.rect.center[0], player.rect.center[1]
    
    mouse_angle_rad = math.atan2(mouse_y - py, mouse_x - px)
    angle_to_mouse = -math.degrees(mouse_angle_rad)

    player.rotate(angle_to_mouse)

    if Engine.MouseClicked(): bullet = Bullet(Engine,"assets/bullet.png", px, py)
    if bullet: bullet.update()

    if Engine.KeyPressed(pygame.K_ESCAPE): Engine.set_active_scene(Menu)

Menu = pge.Scene(Engine)

with Menu.sprites():
    play_button = pge.Button(
        engine=Engine,
        x=SCREEN_W/2, y=SCREEN_H/2,
        img_path="assets/img.png",
        width=150, height=150
    ).place_centered(SCREEN_W/2,SCREEN_H/2)

@Menu.init_scene()
def menu_scene():
    pge.fill_background(engine=Engine, color=pge.Colors.BLACK)

    if play_button.draw(): Engine.set_active_scene(Main)


""" --- 3. Initialize Main function with all your project logics --- """

Engine.set_active_scene(Menu)

@Engine.main()
def main():
    Engine.run_active_scene()

Engine.run()
