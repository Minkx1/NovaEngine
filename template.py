""" ===== template.py ===== """

import pygame, math
import SparkEngine as SE

SCREEN_W, SCREEN_H = 900, 600
MAGAZINE_SIZE = 10

class Zombie(SE.Sprite):
    def __init__(self, engine, img_path, width=None, height=None, speed=150, target = None, killers=None):
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
                if self.target.hp : self.target.hp -= 10
                self.kill()

            if self.killers.collide(self): 
                self.kill()
                self.target.money += 10

            self.draw()
    
class Bullet(SE.Sprite):
    def __init__(self, engine, img_path : str, x: float, y: float, width: float = None, height:float = None, speed: int = 100):
        super().__init__(engine, img_path, width, height, False)

        self.x, self.y = x, y 
        self.place_centered(x, y)

        self.mouse_pos = pygame.mouse.get_pos()
        dx, dy = self.mouse_pos[0] - x, self.mouse_pos[1] - y
        dist = math.hypot(dx, dy)
        if dist == 0: dist = 1

        self.vel_x = dx / dist * speed
        self.vel_y = dy / dist * speed
    
    def move(self, dx, dy):
        super().move(dx, dy)
        self.x,self.y = self.rect.x, self.rect.y

    def update(self):
        if self.alive:
            self.draw()
            self.move(self.vel_x, self.vel_y)
            
            if not self.collide(rect=self.engine.screen.get_rect()):
                self.kill()

class Player(SE.Sprite):
    def __init__(self, engine, img_path, width=None, height=None, speed=5, solids: list[SE.Sprite] = None):
        super().__init__(engine, img_path, width, height, solid=False)
        self.speed = speed
        self.solids = solids
        self.magazine = MAGAZINE_SIZE
        self.shoot:function = None

        self.lvl = 1
        self.hp = 100
        self.money = 0

    def set_shoot(self):
        def wrapper(func):
            self.shoot = func
            return func
        return wrapper

    def update(self):
        SE.TopDownMovement().update(self.engine, self.solids, self)

        self.look_at(pygame.mouse.get_pos())

        if self.engine.MouseClicked() and self.engine.Cooldown('bullet_shoot_cooldown', 0.2):
            self.shoot()
            self.engine.Cooldown('bullet_shoot_cooldown', 0.2, True)

        if self.engine.KeyPressed(pygame.K_r):
            @self.engine.Timer(1)
            def reload(): self.magazine = MAGAZINE_SIZE

        self.draw()
        self.engine.render_text(f"Coins: {self.money}", self.engine.screen.get_width()-110, 35, center=True, size=20)

# ========================
# 1. Initialize Engine
# ========================

Engine = SE.SparkEngine(window_size=(SCREEN_W, SCREEN_H)).set_debug(False)
SaveManager = SE.SaveManager(Engine)

# ========================
# 2. Create Scene
# ========================
Main = SE.Scene(Engine)

with Main.init():
    home_button = SE.Button(Engine, "assets/buttons/Home_Button.png", 50, 50).place_centered(SCREEN_W-35, 35)
    
    player = Player(Engine, "assets/player.png", width=120, height=103, solids=Main.solids).place_centered(SCREEN_W/2, SCREEN_H/2)
    
    bullets = SE.Group()
    zombies = SE.Group()

    hp_bar = SE.ProgressBar(Engine, 250, 75, player.hp, player.hp, bg_color=SE.Colors.RED).set_position(10, SCREEN_H-85)
    @hp_bar.set_update()
    def hp_bar_upd():
        hp_bar.draw()
        hp_bar.set_value(player.hp)

    @player.set_shoot()
    def shoot_bullet():
        if player.magazine > 0:
            bullets.add(Bullet(Engine, 'assets/bullet.png', player.rect.centerx, player.rect.centery, 8, 8))
            player.magazine -= 1
Menu = SE.Scene(Engine)

with Menu.init():
    play_button = SE.Button(Engine, "assets/buttons/Play_Button.png", 300, 100).place_centered(SCREEN_W/2, 100)
    quit_button = SE.Button(Engine, "assets/buttons/Quit_Button.png", 300, 100).place_centered(SCREEN_W/2, 220)
    bg = SE.Sprite.CreateImage("assets/menu_bg.png", SCREEN_W, SCREEN_H)

# ========================
# 3. Scene logic
# ========================
@Main.logic()
def main_logic():
    Engine.fill_background(SE.Colors.WHITE)

    if home_button.check(): Engine.set_active_scene(Menu)
    if Engine.KeyPressed(pygame.K_ESCAPE): Engine.set_active_scene(Menu)
    
    Main.update()

    Engine.render_text(f"Round: {player.magazine}", SCREEN_W-70, SCREEN_H-20, size=30, color=SE.Colors.RED, center=True)

@Menu.logic()
def menu_logic():
    Engine.fill_background(image=bg)
    if quit_button.check(): Engine.quit()
    if play_button.check(): Engine.set_active_scene(Main)

# ========================
# 4. Run Engine
# ========================

@Engine.Interval(3, 2)
def zombie_spawn():
    zombies.add(Zombie(Engine, "assets/zombie.png", width=106, height=98, target=player, killers=bullets).place_centered(75, 75))

SaveManager.set_vars(["player.rect.x", "player.rect.y", "player.hp", "player.money"])

SaveManager.load()

Engine.set_active_scene(Menu)
Engine.run()

SaveManager.save()

# SE.DevTools.build_exe(main_file="template.py", name="app", noconsole=True)