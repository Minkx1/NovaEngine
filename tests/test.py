import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # making python see novaengine/

import pygame
import novaengine as nova

SCREEN_W, SCREEN_H = (500, 500)

app = nova.NovaEngine((SCREEN_W, SCREEN_H), "NovaTest", "assets/icon.png", 60).set_debug(True)

class Player(nova.Sprite):
    def __init__(self, img_path, width = None, height = None, speed=5, solid=False):
        super().__init__(img_path, width, height, solid)
        self.speed = speed
    
        self.ground = int(SCREEN_H*0.85)
        self.gravity = 1
        self.jump_strength = 20
        self.vx, self.vy = (0, 0)
        self.vel_cap = 10

    def update(self):
        if self.alive:
            self.draw()

            dx, dy = (0, 0)
            if not self._on_ground():
                self.vy += self.gravity
            else:
                self.vy = 0

            if app.KeyPressed(pygame.K_SPACE):
                self._jump()
            if app.KeyHold(pygame.K_a): self.vx -= self.speed/10
            if app.KeyHold(pygame.K_d): self.vx += self.speed/10

            #capping
            self.vx = self._cap_vel(self.vx)

            if not (app.KeyHold(pygame.K_a) or app.KeyHold(pygame.K_d)):
                if self.vx>=0: 
                    self.vx = max(0, self.vx-self.speed)
                if self.vx<0: 
                    self.vx = min(0, self.vx+self.speed)

            self.move(dx+self.vx, dy+self.vy)
            self.stay_in_rect(app.screen.get_rect()) 

    def _cap_vel(self, vel):
        if vel < 0:
            return -min(self.vel_cap, abs(vel))
        elif vel >= 0:
            return min(self.vel_cap, vel)

    def _on_ground(self):
        return self.y + self.height >= self.ground

    def _jump(self):
        if self._on_ground():
            self.vy -= self.jump_strength

s = nova.Scene()
with s.sprites():
    test_sprite = Player("assets/player.png", 75, 75).set_position(100, 100)

@s.function()
def _():
    s.update()

@app.main()
def main():
    nova.Utils.fill_background(nova.Colors.WHITE)
    app.run_active_scene()

app.run()