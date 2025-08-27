import pygame
import SparkEngine as SE

SCREEN = (500, 500)
Engine = SE.SparkEngine(SCREEN, "TestSparkEngine", "assets/button.png").set_debug(True)
PLAYER_SPEED = 5

player = SE.Sprite(Engine, "assets/player.png", 120, 103)
target = SE.Sprite(Engine, "assets/hero.png", 100, 100).place_centered(SCREEN[0]/2, SCREEN[1]/2)
bullets = SE.Group()

@player.set_update()
def P_UPD():

    if Engine.KeyHold(pygame.K_w): player.move(dy=-PLAYER_SPEED)
    if Engine.KeyHold(pygame.K_s): player.move(dy=PLAYER_SPEED)
    if Engine.KeyHold(pygame.K_a): player.move(dx=-PLAYER_SPEED)
    if Engine.KeyHold(pygame.K_d): player.move(dx=PLAYER_SPEED)

    # staying in bounds
    if player.rect.left < 0 : player.rect.left = 0
    if player.rect.right > SCREEN[0] : player.rect.right = SCREEN[0]
    if player.rect.top < 0 : player.rect.top = 0
    if player.rect.bottom > SCREEN[1] : player.rect.bottom = SCREEN[1]

    if Engine.MouseClicked():
        bullet = SE.Sprite(Engine, "assets/bullet.png", 8, 8).place_centered(player.rect.centerx, player.rect.centery)
        bullet.look_at(target)
        @bullet.set_update()
        def _():
            if not bullet.collide(rect=Engine.screen.get_rect()): 
                bullet.kill()
            bullet.draw()
            bullet.move_angle(50)
        bullets.add(bullet)    

    player.look_at(pygame.mouse.get_pos())
    player.draw()


@Engine.main()
def main():
    Engine.fill_background((250, 250, 250))
    player.update()
    target.update()
    bullets.update()
    print(len(bullets))

Engine.run()