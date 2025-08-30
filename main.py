import pygame, random, NovaEngine as nova

SCREEN_W, SCREEN_H = 900, 650
GUIPANEL_H = 50
PLAYER_SPD = 5

Engine = nova.NovaEngine((SCREEN_W, SCREEN_H), "TestGame", "assets/hero.png").set_debug(True)
saves = nova.SaveManager(Engine, path="ZombieKillerGame", name="data")

class Player(nova.Sprite):
    def __init__(self, engine, img_path, width=None, height=None, speed=5):
        super().__init__(engine, img_path, width, height, solid=False)
        self.speed = speed

        self.hp = 100
        self.money = 0
        self.max_magazine = 10
        self.magazine = self.max_magazine

        self.projectiles = nova.Group()

    def update(self):
        self.projectiles.update()

        self.draw()
        self.look_at(pygame.mouse.get_pos())

        if self.engine.KeyHold(pygame.K_w):
            self.move(dy=-self.speed)
        if self.engine.KeyHold(pygame.K_s):
            self.move(dy=self.speed)
        if self.engine.KeyHold(pygame.K_a):
            self.move(dx=-self.speed)
        if self.engine.KeyHold(pygame.K_d):
            self.move(dx=self.speed)

        self.stay_in_rect(pygame.rect.Rect(0, GUIPANEL_H, SCREEN_W, SCREEN_H-GUIPANEL_H))

        if self.engine.MouseClicked():
            self.shoot()
        
        if self.engine.KeyPressed(pygame.K_r):
            self.reload()

    def shoot(self):
        if self.magazine > 0:
            p = nova.Projectile(
                self.engine, "assets/bullet.png",
                8,8,
                self.rect.center, pygame.mouse.get_pos()
            )
            self.projectiles.add(p)
            self.magazine -= 1
    
    def reload(self):
        @self.engine.Timer(1)
        def _():
            self.magazine = self.max_magazine


class Zombie(nova.Sprite):
    def __init__(
        self,
        engine,
        img_path,
        width=None,
        height=None,
        speed=150,
        target=None,
        killers=None,
    ):
        super().__init__(engine, img_path, width, height, solid=True)
        self.speed = speed

        self.target = target
        self.killers = killers

    def update(self):
        if self.alive:
            self.look_at(self.target)

            if not self.collide(self.target):
                self.move_to(self.target, self.speed)
            else:
                if self.target.hp:
                    self.target.hp -= 10
                self.kill()

            if self.killers.collide(self):
                for k in self.killers:
                    if k.collide(self):
                        k.kill()
                        break
                self.kill()
                self.target.money += 10

            self.draw()

# Main Scene
Main = nova.Scene(Engine)
with Main.sprites():
    main_bg_img = nova.Sprite.CreateImage("assets/main_bg.png", SCREEN_W, SCREEN_H)

    player = Player(Engine, "assets/player.png", 120, 120).place_centered(SCREEN_W / 2, SCREEN_H / 2)
    zombies = nova.Group()

    hp_bar = nova.ProgressBar(Engine, 300, 50, 100, 100, (200, 0, 0)).bind("player.hp")
    money_text = nova.TextLabel(Engine, 390, 25, "Money: $",size=24, color=nova.Colors.WHITE, center=True).bind('player.money')
    magazine_text = nova.TextLabel(Engine, 540, 25, text="  |  Magazine: ", size = 24, color=nova.Colors.WHITE, center=True).bind("player.magazine")
        
@Main.function()    
def _():
    # Engine.fill_background(image=main_bg_img)
    pygame.draw.rect(Engine.screen, nova.Colors.BLACK, (0, 0, SCREEN_W, GUIPANEL_H))

    if Engine.KeyPressed(pygame.K_ESCAPE): Engine.set_active_scene(Menu)
    
    Main.update() 

# Menu Scene
Menu = nova.Scene(Engine)
with Menu.sprites():
    menu_bg_img = nova.Sprite.CreateImage("assets/menu_bg.png", SCREEN_W, SCREEN_H)

    play_btn = nova.Button(Engine, "assets/Buttons/Play_Button.png", 300, 100).place_centered(SCREEN_W/2, 160)
    options_btn = nova.Button(Engine, "assets/Buttons/Options_Button.png", 300, 100).place_centered(SCREEN_W/2, 280)
    quit_btn = nova.Button(Engine, "assets/Buttons/Quit_Button.png", 300, 100).place_centered(SCREEN_W/2, 400)

@Menu.function()
def _():
    Engine.fill_background(image=menu_bg_img)
    
    if play_btn.check(): Engine.set_active_scene(Main)
    if quit_btn.check(): Engine.quit()

    Menu.update()

# Main Game Cycle
@Engine.Interval(10, 1)
def zombie_spawn():
    side = random.choice(["left", "right", "top", "bottom"])

    if side == "left":
        x, y = -50, random.randint(0, SCREEN_H)   
    elif side == "right":
        x, y = SCREEN_W + 50, random.randint(0, SCREEN_H)
    elif side == "top":
        x, y = random.randint(0, SCREEN_W), -50
    else: 
        x, y = random.randint(0, SCREEN_W), SCREEN_H + 50

    zombies.add(
        Zombie(Engine,"assets/zombie.png",106,98,target=player,killers=player.projectiles).place_centered(x, y)
    )

saves.set_vars(["player.money"])

saves.load()

Engine.run(Main)

saves.save()