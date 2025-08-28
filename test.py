import pygame, NovaEngine as nova

SCREEN = (500, 500)
Engine = nova.NovaEngine((500, 500), "TEST", "assets/button.png").set_debug(False)

s = nova.Scene(Engine)
with s.sprites():
    player = nova.Sprite(Engine, "assets/player.png", 120, 103); player.hp = 100
    bullets = nova.Group()

    # input1 = nova.Input(Engine, 50, 400, color=nova.Colors.BLACK, bg_color=(250, 250, 250))
    label1 = nova.TextLabel(Engine, SCREEN[0]-50, 50, "ПІСЮНИ", center=True)
    checkbox = nova.CheckBox(Engine, 50, SCREEN[1]-50, 30, 30, "Are you Gay?", state=True)

    @player.set_update()
    def P_UPD():
        t = pygame.mouse.get_pos()
        nova.simpleTopDown(speed=5).update(Engine, player)
        player.stay_in_rect(Engine.screen.get_rect())
        player.look_at(t)
        player.draw()

        if Engine.MouseClicked(): bullets.add(nova.Projectile(Engine, "assets/bullet.png", 8, 8, player.rect.center, t))    

Engine.run()