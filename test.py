import pygame
import NovaEngine as nova

SCREEN = (500, 500)
Engine = nova.NovaEngine(SCREEN, "TestNovaEngine", "assets/button.png").set_debug(True)

player = nova.Sprite(Engine, "assets/player.png", 120, 103)
bullets = nova.Group()

@player.set_update()
def P_UPD():

    nova.simpleTopDown(speed=5).update(Engine, player)

    player.stay_in_rect(Engine.screen.get_rect())

    player.look_at(pygame.mouse.get_pos())
    player.draw()

@Engine.main()
def main():
    Engine.fill_background((250, 250, 250))
    if Engine.MouseClicked(): 
        bullets.add(nova.Projectile(Engine, "assets/bullet.png", 8, 8, start=player.rect.center, target=pygame.mouse.get_pos()))  
    bullets.update()
    player.update()    

Engine.run()