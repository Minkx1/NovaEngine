import pygame, random, NovaEngine as nova

# ========================================= #

""" # ===== #   INITIALIZATION  # ===== # """

# ========================================= #

SCREEN_W, SCREEN_H = 900, 650
GUIPANEL_H = 50

Engine = nova.NovaEngine((SCREEN_W, SCREEN_H), "Kill 'Till Dawn", "assets/icon.png").set_debug(False)
sounds = nova.SoundManager()
saves = nova.SaveManager(Engine, path="ZombieKillerGame", name="data").set_vars(["player.money", "Engine.record_time", "player.max_hp"])

sounds.load_sound("shot", "assets/gun_shot.mp3")

""" # ===== #   ADDITIONAL CLASSES  # ===== # """


class Player(nova.Sprite):
    def __init__(self, engine, img_path, width=None, height=None, speed=5):
        super().__init__(engine, img_path, width, height, solid=False)
        self.speed = speed
        self.start_pos = (self.x, self.y)

        self.max_hp = saves.get_value("player.max_hp") or 100
        self.hp = self.max_hp
        self.money = saves.get_value("player.money") or 10

        self.max_magazine = 10
        self.magazine = self.max_magazine
        self.player_alive = True
        self.immortal = False

        self.projectiles = nova.Group()

        frames = []
        for i in range(20):
            frames.append(nova.Sprite.CreateImage(f"assets/player/survivor-move_handgun_{i}.png", self.width, self.height))
        self.set_animation(
            name = "walk",
            frames=frames,
            speed=0.05
        )

    def update(self):
        self.projectiles.update()

        self.draw()
        self.look_at(pygame.mouse.get_pos())
        self.play_animation("walk")

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
        
        if player.hp <= 0:
            self.player_alive = False

    def shoot(self):
        if self.magazine > 0:
            p = nova.Projectile(
                self.engine, "assets/bullet.png",
                8,8,
                self.rect.center, pygame.mouse.get_pos()
            )
            self.projectiles.add(p)
            self.magazine -= 1

            sounds.play_sound("shot", 0.25)
    
    def reload(self):
        @self.engine.Timer(1)
        def _():
            self.magazine = self.max_magazine
    
    def respawn(self):
        self.player_alive = True
        self.alive = True
        self.hp = self.max_hp
        self.magazine = self.max_magazine
        self.x, self.y = self.start_pos


class Zombie(nova.Sprite):
    def __init__(
        self,
        engine,
        img_path,
        width=None,
        height=None,
        speed=150, hp=10,
        target=None,
        killers=None,
    ):
        super().__init__(engine, img_path, width, height, solid=True)
        self.speed = speed

        self.target = target
        self.killers = killers
        self.hp = hp

        nova.Sprite._counter -= 1
        self.count = 0

        frames = []
        for i in range(16):
            frames.append(nova.Sprite.CreateImage(f"assets/zombie/skeleton-move_{i}.png", self.width, self.height))
        self.set_animation(
            name = "walk",
            frames=frames,
            speed=0.035
        )

    def update(self):
        if self.alive:
            self.look_at(self.target)
            self.play_animation("walk")

            if not self.collide(self.target):
                self.move_to(self.target, self.speed)
            else:
                if self.target.hp and not self.target.immortal:
                    self.target.hp -= 10
                self.hp -= 10

            if self.killers.collide(self):
                for k in self.killers:
                    if k.collide(self):
                        k.kill()
                        break
                self.hp -= 10
                self.target.money += 10

            if self.hp <= 0: self.kill()

# ================================= #

""" # ===== #   SCENES  # ===== # """

# ================================= #

# Main Scene
Main = nova.Scene(Engine)
with Main.sprites():
    Engine.record_time = 0

    # main_bg = nova.Sprite(Engine, "assets/main_bg.png", SCREEN_W, SCREEN_H)
    panel = nova.Rect(Engine, rect=(0, 0, SCREEN_W, GUIPANEL_H))

    player = Player(Engine, "assets/player.png", 120, 120).place_centered(SCREEN_W / 2, SCREEN_H / 2)

    zombies = nova.Group()
    zombie_cd = Engine.create_cooldown(2)
    def zombie_spawn():
        side = random.choice(["left", "right", "bottom"])

        if side == "left":
            x, y = -50, random.randint(0, SCREEN_H)   
        elif side == "right":
            x, y = SCREEN_W + 50, random.randint(0, SCREEN_H)
        else: 
            x, y = random.randint(0, SCREEN_W), SCREEN_H + 50

        hit_points = 10 #max(10, (15*Engine.time//15000))
        zombey = Zombie(Engine,"assets/zombie.png",115,115,hp=hit_points, target=player,killers=player.projectiles).place_centered(x, y)
        
        zombies.add(zombey)
    
    hp_bar = nova.ProgressBar(Engine, 300, 50, player.max_hp, player.hp, (200, 0, 0))
    @hp_bar.set_update()
    def _():
        hp_bar.draw()
        hp_bar.set_max_value(player.max_hp)
        hp_bar.set_value(player.hp)

    money_text = nova.TextLabel(Engine, 390, 25, "Money: $",size=24, color=nova.Colors.WHITE, center=True).bind('player.money')
    magazine_text = nova.TextLabel(Engine, 540, 25, text="  |  Magazine: ", size = 24, color=nova.Colors.WHITE, center=True).bind("player.magazine")
    time_text = nova.TextLabel(Engine, 690, 25, " |  Time: ", size=24, color=nova.Colors.WHITE, center=True).bind("Engine.in_game_time")
    @time_text.modify_value()
    def _(var):
        sec = var//1000
        return f" {sec//60} : {sec%60}"

@Main.function()    
def _():
    Engine.fill_background(color=nova.Colors.WHITE)

    if Engine.KeyPressed(pygame.K_ESCAPE): Engine.set_active_scene(Pause)
    if zombie_cd.check():
        zombie_spawn()
        zombie_cd.start()
    
    if not player.player_alive:
        player.kill()
        Engine.set_active_scene(Death)

    Main.update() 

# Pause Scene
Pause = nova.Scene(Engine)
with Pause.sprites():
    txt1 = nova.TextLabel(Engine, SCREEN_W/2, 150, "G A M E       P A U S E D",size=32, color=nova.Colors.WHITE, center=True)
    resume_btn = nova.Button(Engine, "assets/Buttons/Resume_Button.png", 300, 100).place_centered(SCREEN_W/2, 250)
    menu_btn = nova.Button(Engine, "assets/Buttons/Menu_Button.png", 300, 100).place_centered(SCREEN_W/2, 400)

@Pause.function()
def _():
    Engine.time_freeze()
    Engine.fill_background(nova.Colors.BLACK)
    
    if resume_btn.check():
        Engine.time_unfreeze()
        Engine.set_active_scene(Main)
    if menu_btn.check():
        Engine.set_active_scene(Menu)

    Pause.update()

# Death Scene
Death = nova.Scene(Engine)
with Death.sprites():
    death_bg = nova.Rect(Engine, rect=(0,0,SCREEN_W,SCREEN_H))

    death_txt = nova.TextLabel(Engine, SCREEN_W/2, 60, "Y O U    D I E D", size=90, color=nova.Colors.WHITE, center=True)
    survived = nova.TextLabel(Engine, SCREEN_W/2, 140, "You Survived - ", size=36, color=nova.Colors.WHITE, center=True).bind("Engine.in_game_time")
    @survived.modify_value()
    def _(val):
        sec = val//1000
        return f"{sec//60} : {sec%60}" 
    
    record_death_txt = nova.TextLabel(Engine, SCREEN_W/2, 200, "Your Record - ", size=36, color=nova.Colors.WHITE, center=True).bind("Engine.record_time")
    @record_death_txt.modify_value()
    def _(val) -> str:
        sec = val//1000
        return f"{sec//60} : {sec%60}"

    menu_button = nova.Button(Engine, "assets/Buttons/Menu_Button.png", 300, 100).place_centered(SCREEN_W/2, 300)

@Death.function()
def _():
    Engine.time_freeze()

    if menu_button.check():
        player.respawn()
        Engine.set_active_scene(Menu)

    Death.update()

# Options Scene
Options = nova.Scene(Engine)
with Options.sprites():
    opts_bg = nova.Sprite(Engine, "assets/menu_bg.png", SCREEN_W, SCREEN_H)
    record_text = nova.TextLabel(Engine, SCREEN_W/2, 75, "There is nothing to see here. GO AND KILL ZOMBIES!!!", size=32, color=nova.Colors.WHITE, center=True)
    menu_buttn = nova.Button(Engine, "assets/Buttons/Menu_Button.png", 300, 100).place_centered(SCREEN_W/2, 520)

@Options.function()
def _():
    if menu_buttn.check(): Engine.set_active_scene(Menu)

    Options.update()

# Menu Scene
Menu = nova.Scene(Engine)
with Menu.sprites():
    menu_bg_img = nova.Sprite(Engine, "assets/menu_bg.png", SCREEN_W, SCREEN_H)

    record_text = nova.TextLabel(Engine, SCREEN_W/2, 50, "RECORD TIME - ", size=36, color=nova.Colors.WHITE, center=True).bind("Engine.record_time")
    @record_text.modify_value()
    def _(val: int) -> str:
        sec = val//1000
        return f"{sec//60} : {sec%60}"

    play_btn = nova.Button(Engine, "assets/Buttons/Play_Button.png", 300, 100).place_centered(SCREEN_W/2, 160)
    options_btn = nova.Button(Engine, "assets/Buttons/Options_Button.png", 300, 100).place_centered(SCREEN_W/2, 280)
    shop_btn = nova.Button(Engine, "assets/Buttons/Shop_Button.png", 300, 100).place_centered(SCREEN_W/2, 400)
    quit_btn = nova.Button(Engine, "assets/Buttons/Quit_Button.png", 300, 100).place_centered(SCREEN_W/2, 520)

@Menu.function()
def _():
    Engine.time_freeze()
    
    if play_btn.check(): 
        Engine.set_active_scene(Main)
        Engine.time_unfreeze()
    if options_btn.check():
        Engine.set_active_scene(Options)
    if shop_btn.check(): Engine.set_active_scene(Shop)
    if quit_btn.check(): Engine.quit()

    Menu.update()

Shop = nova.Scene(Engine)
with Shop.sprites():
    shop_bg = nova.Rect(Engine, rect=(0,0,SCREEN_W, SCREEN_H))
    money_txt = nova.TextLabel(Engine, SCREEN_W/2, 25, "Money: $", size=32, color=nova.Colors.WHITE, center=True).bind("player.money")

    hp_up = nova.Button(Engine, "assets/Buttons/upgrade.png", 48, 48).place_centered(SCREEN_W/2 + 100, SCREEN_H/2)
    player.hp_cost = int(100 * ((player.max_hp / 100) ** 1.85))
    hp_up_txt = nova.TextLabel(Engine, SCREEN_W/2-150, SCREEN_H/2, "Max HP Upgrade: $",size=32,center=True, color=nova.Colors.WHITE).bind("player.hp_cost")
    hp_txt =nova.TextLabel(Engine, SCREEN_W/2-150, SCREEN_H/2+50, "HP lvl: ",size=32,center=True, color=nova.Colors.WHITE).bind("player.max_hp")

@Shop.function()
def _():
    Engine.time_freeze()

    if Engine.KeyPressed(pygame.K_ESCAPE): Engine.set_active_scene(Menu)
    if hp_up.check():
        player.hp_cost = int(100 * ((player.max_hp / 100) ** 1.85))
        if player.money < player.hp_cost:
            pop = nova.Popup(Engine, text = "Not Enough Money!", x = pygame.mouse.get_pos()[0]+random.randint(-5, 5), y = pygame.mouse.get_pos()[1]-40+random.randint(-5, 5), time=2, color=nova.Colors.WHITE)
            Shop.add_sprite(pop)
        else:
            player.money-=player.hp_cost
            player.max_hp += 10

    Shop.update()


# ===================================================== #

""" # ===== #   MAIN FUNCTION AND GAME RUN  # ===== # """

# ===================================================== #


@Engine.main()
def main():
    Engine.run_active_scene()
    Engine.record_time = max(Engine.in_game_time, Engine.record_time)

Engine.run(first_scene=Menu, save_manager=saves)

# nova.DevTools.build_archive(
#     name="ZombieKiller",
#     icon_path="assets/icon.ico",
#     noconsole=True,
#     sprite_dir="assets",
#     archive_name="ZombieKiller_V1_0_0_alpha.zip"
# )