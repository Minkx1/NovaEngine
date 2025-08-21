""" ===== template.py ===== """

import pygame, math,subprocess,sys
import PyGameEngine as pge

from bullet import Bullet

""" --- 1. Initialize PyGameEngine --- """

SCREEN_W, SCREEN_H = 900, 600 
PLAYER_SPEED = 5

Engine = pge.PyGameEngine()
Engine.init(window_size=(900, 600))

bullet = None

""" --- 2. Create Scene, Add assets and Initialize function --- """

Scene1 = pge.Scene(Engine)

with Scene1.sprites():
    player = pge.Sprite(
        engine=Engine,img_path="assets/player.png",
        width=120, height=103
    ).place_centered(SCREEN_W/2, SCREEN_H/2)


@Scene1.init_scene()
def scene1():
    pge.fill_background(engine=Engine, color=(225, 225, 225))

    # PLAYER LOGIC
    @player.set_update
    def player_draw(self):
        global bullet
        if Engine.KeyPressed(pygame.K_w): self.move(0, -PLAYER_SPEED)
        if Engine.KeyPressed(pygame.K_s): self.move(0, PLAYER_SPEED)
        if Engine.KeyPressed(pygame.K_a): self.move(-PLAYER_SPEED)
        if Engine.KeyPressed(pygame.K_d): self.move(PLAYER_SPEED)

        mouse_x,mouse_y = pygame.mouse.get_pos()
        px,py = self.rect.center[0], self.rect.center[1]
        
        mouse_angle_rad = math.atan2(mouse_y - py, mouse_x - px)
        angle_to_mouse = -math.degrees(mouse_angle_rad)
        self.rotate(angle_to_mouse)
        if Engine.MouseClicked(): bullet = Bullet(
            Engine, 'assets/bullet.png',
            x = px, y = py,
            width = 8, height = 8
            )
        if bullet: bullet.update()

        self.draw()

    Scene1.update()


""" --- 3. Initialize Main function with all your project logics --- """

@Engine.main()
def main():
    Engine.run_active_scene()

@pge.thread()
def run_cmd_input():
    while True:
        cmd = input(">>> ")
        if cmd == "kill()":
            Engine.kill()
            break
        elif cmd == "restart()":
            subprocess.Popen([sys.executable] + sys.argv)
            Engine.kill()
            break
        try:
            eval(cmd)
        except Exception as e:
            print("Error:", e)

Engine.run()
