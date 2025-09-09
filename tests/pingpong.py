import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # making python see novaengine/

import pygame
import random
import novaengine as nova

SCREEN_W, SCREEN_H = (750, 500)

app = nova.NovaEngine((SCREEN_W, SCREEN_H), "NovaTest", "assets/icon.png", 60).set_debug(True)

class Panel(nova.Sprite):
    def __init__(self, img_path, width = None, height = None, movement="w", ball=None):
        super().__init__(img_path, width, height, True)
        self.movement = movement
        self.speed = 10
        self.ball = ball
        if self.movement=="w":
            self.x = 20
            self.place_centered(self.x+self.width/2, SCREEN_H/2)
        elif self.movement=="^":
            self.x = SCREEN_W-20
            self.place_centered(self.x-self.width/2, SCREEN_H/2)

    def draw(self):
        if self.img: super().draw()
        else:
            pygame.draw.rect(self.surface, (0,0,0), (self.x, self.y, self.width, self.height))

    def update(self):
        if self.alive:
            self.draw()

            dy = 0
            if self.movement == "w":
                if self.engine.KeyHold(pygame.K_w): dy -= self.speed
                if self.engine.KeyHold(pygame.K_s): dy += self.speed
            elif self.movement == "^":
                if self.engine.KeyHold(pygame.K_UP): dy -= self.speed
                if self.engine.KeyHold(pygame.K_DOWN): dy += self.speed

            self.move(0, dy)
            self.stay_in_rect(self.surface.get_rect())

            self.ball.rect = pygame.Rect(self.ball.x, self.ball.y, self.ball.radius*2, self.ball.radius*2)

            if self.collide(self.ball):
                self.ball.vel_x = -self.ball.vel_x
                self.ball.vel_y = -self.ball.vel_y

class Ball(nova.Sprite):
    def __init__(self, img_path=None, width = None, height = None, vel_x=5, vel_y=5):
        super().__init__(img_path, width, height, True)

        self.vel_x, self.vel_y = vel_x, vel_y
        self.radius = 15
        self.height = 2*self.radius
        self.width = 2*self.radius
    
    def draw(self):
        pygame.draw.circle(self.surface, (255, 0, 0), (self.x+self.width/2, self.y+self.height/2), self.radius)

    def update(self):
        if self.alive:
            self.draw()
            self.move(self.vel_x, self.vel_y)

            if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_W:
                self.vel_x = -self.vel_x  # змінюємо напрямок по X
            if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_H:
                self.vel_y = -self.vel_y  # змінюємо напрямок по Y

s = nova.Scene()
with s.sprites():

    ball = Ball(vel_x=random.choice([-1, 1])*random.randint(3, 5), vel_y=random.choice([-1, 1])*random.randint(3, 5)).place_centered(SCREEN_W/2, SCREEN_H/2)
    
    l_pan = Panel(None, 50, 200, "w", ball)
    r_pan = Panel(None, 50, 200, "^", ball)    

app.run()