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

    # PLAYER LOGIC
    @player.set_update
    def player_update(self):
        global bullet
        # Moving and collision
        dx, dy = 0, 0
        if pge.KeyHold(pygame.K_w): dy -= PLAYER_SPEED
        if pge.KeyHold(pygame.K_s): dy += PLAYER_SPEED
        if pge.KeyHold(pygame.K_a): dx -= PLAYER_SPEED
        if pge.KeyHold(pygame.K_d): dx += PLAYER_SPEED

        # X
        self.move(dx, dy)
        for s in Scene1.solids:
            if self.collide(s):
                # відкотимо назад по X
                self.move(-dx, 0)
                dx = 0
                break

        # Y
        self.move(0, dy)
        for s in Scene1.solids:
            if self.collide(s):
                # відкотимо назад по Y
                self.move(0, -dy)
                dy = 0
                break

        mouse_x,mouse_y = pygame.mouse.get_pos()
        px,py = self.rect.center[0], self.rect.center[1]
        
        mouse_angle_rad = math.atan2(mouse_y - py, mouse_x - px)
        angle_to_mouse = math.degrees(mouse_angle_rad)
        self.rotate(angle_to_mouse)
        if pge.MouseClicked(): bullet = Bullet(Engine, 'assets/bullet.png', px, py, 8,8)
        if bullet: bullet.update()

        self.draw()

    Scene1.update()

""" --- 3. Initialize Main function with all your project logics --- """

Engine.run(globals())
