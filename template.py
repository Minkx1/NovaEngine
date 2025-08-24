""" ===== template.py ===== """

import pygame
import SparkEngine as SE
from bullet import Bullet

# ========================
# 1. Initialize Engine
# ========================
SCREEN_W, SCREEN_H = 900, 600
PLAYER_SPEED = 5
MAGAZINE_SIZE = 10

Engine = SE.SparkEngine(window_size=(SCREEN_W, SCREEN_H)).set_debug(False)
SaveManager = SE.SaveManager(Engine)

# ========================
# 2. Create Scene
# ========================
Main = SE.Scene(Engine)

with Main.init():
    home_button = SE.Button(Engine, "assets/buttons/Home_Button.png", 50, 50).place_centered(SCREEN_W-35, 35)

    player = SE.Sprite(Engine, "assets/player.png", width=120, height=103).place_centered(SCREEN_W/2, SCREEN_H/2)
    player.magazine = MAGAZINE_SIZE

    bullets = SE.Group()

    def shoot_bullet():
        if player.magazine > 0:
            bullets.add(Bullet(Engine, 'assets/bullet.png', player.rect.centerx, player.rect.centery, 8, 8))
            player.magazine -= 1

    @player.set_update()
    def update_player():
        SE.ZombieKillerMovement().update(Engine, Main.solids, player)

        if Engine.MouseClicked():
            shoot_bullet()

        if Engine.KeyPressed(pygame.K_r):
            @Engine.Timer(1)
            def reload(): player.magazine = MAGAZINE_SIZE

        # Remove dead bullets safely
        to_remove = [b for b in bullets if not b.alive]
        for b in to_remove:
            bullets.remove(b)

        player.draw()

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

    if home_button.check():Engine.set_active_scene(Menu)
    
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

SaveManager.set_vars(["player.rect.x", "player.rect.y", "player.magazine"])

SaveManager.load()

Engine.set_active_scene(Menu)
Engine.run()

SaveManager.save()

# SE.DevTools.build_exe(main_file="template.py", name="app", noconsole=True)