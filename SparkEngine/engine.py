""" ===== engine.py ===== """

import pygame, threading, sys, subprocess, time
from typing import Tuple, Union
from enum import Enum

pygame.init()

# ========================
# ENGINE CONSTANTS
# ========================
ENGINE_VERSION = "V1.5.2"
APP_NAME_ENGINE_TEMPLATE = f" | Running with SparkEngine {ENGINE_VERSION}"

# ========================
# BASIC COLORS
# ========================
class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)


class SparkEngine:
    """
    Lightweight PyGame framework for game loop, input handling, scenes, threads, timers, and text rendering.
    """

    # ========================
    # INITIALIZATION
    # ========================
    def __init__(self, window_size=(500, 500), app_name="Game", icon_path=None, fps=60, show_fps=False):
        """Initialize game window, clock, engine state."""
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(app_name + APP_NAME_ENGINE_TEMPLATE)

        if icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.show_fps = show_fps
        self.m_clck = False

        self.keys_pressed = []
        self.key_single_state = {}

        self._text_cache = {}
        self.cooldowns = {}
        self.intervals = []

        self.scenes = []
        self.active_scene = None
        self.main_run_func = self.run_active_scene

        self.threads = []
        self.cmd_allow = True
        self.running = False

    # ========================
    # MAIN LOOP
    # ========================
    def run(self, main_globals=None):
        """Run the main game loop and optional command input thread."""
        self.console_vars = main_globals or {}

        # Start command input thread
        if self.cmd_allow:
            @self.new_thread()
            def run_cmd_input():
                while True:
                    cmd = input(">>> ")
                    if cmd == "kill()":
                        self.quit()
                        break
                    elif cmd == "restart()":
                        subprocess.Popen([sys.executable] + sys.argv)
                        self.quit()
                        break
                    try:
                        exec(cmd, getattr(self, "console_vars", {}))
                    except Exception as e:
                        print("Error:", e)

        self.running = True
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()

            # Execute main user logic
            if self.main_run_func: self.main_run_func()

            # Show FPS
            if self.show_fps: self.render_text(f"{round(self.clock.get_fps(), 2)}", 5, 5)

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(self.fps)

    def quit(self):
        """Stop engine and exit program."""
        self.running = False
        print("[SparkEngine] Quitting the game")
        sys.exit()

    def main(self):
        """Decorator to register main game logic."""
        def decorator(func):
            self.main_run_func = func
            return func
        return decorator

    def new_thread(self):
        """Decorator to register a function to run in a separate daemon thread."""
        def decorator(func):
            if func not in self.threads:
                self.threads.append(func)
                threading.Thread(target=func, daemon=True).start()
            return func
        return decorator

    # ========================
    # SCENE MANAGEMENT
    # ========================
    def run_scene(self, scene):
        """Run a specific registered scene."""
        if scene in self.scenes:
            self.active_scene = scene
            scene.run()
        else:
            print("[SparkEngine] Scene not found!")

    def run_active_scene(self):
        if self.active_scene:
            self.active_scene.run()

    def set_active_scene(self, scene):
        self.active_scene = scene

    # ========================
    # INPUT MANAGEMENT
    # ========================
    def MouseClicked(self, button=0):
        """Return True only on first mouse click (not hold)."""
        pressed = False
        if not self.m_clck and pygame.mouse.get_pressed()[button]:
            self.m_clck = True
            pressed = True
        if not pygame.mouse.get_pressed()[button]:
            self.m_clck = False
        return pressed

    def KeyPressed(self, key):
        """Return True only on first key press (not hold)."""
        try:
            pressed = bool(self.keys_pressed[key])
        except (IndexError, TypeError):
            return False

        if pressed:
            if not self.key_single_state.get(key, False):
                self.key_single_state[key] = True
                return True
            return False
        else:
            self.key_single_state[key] = False
            return False

    def KeyHold(self, key):
        """Return True while key is held."""
        try:
            return bool(self.keys_pressed[key])
        except (IndexError, TypeError):
            return False

    # ========================
    # TIME MANAGEMENT
    # ========================
    def Timer(self, duration):
        """Decorator to run function after duration seconds."""
        def decorator(func):
            threading.Timer(duration, func).start()
            return func
        return decorator

    def Cooldown(self, key, duration, force=False):
        """Check or create a cooldown for a key."""
        if self.cooldowns.get(key) is None or force:
            @self.new_thread()
            def _():
                self.cooldowns[key] = False
                time.sleep(duration)
                self.cooldowns[key] = True
        return self.cooldowns.get(key, False)

    # ========================
    # UTILITIES
    # ========================
    def fill_background(self, color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK, image: pygame.Surface = None):
        """Fill the screen with a color or an image."""
        if image:
            self.screen.blit(image, (0, 0))
        else:
            if isinstance(color, Colors):
                color = color.value
            self.screen.fill(color)

    def render_text(self, text: str, x: float, y: float, font: str = "TimesNewRoman", size: int = 14,
                    color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK, center: bool = False):
        """Render text on screen with caching."""
        if isinstance(color, Colors):
            color = color.value

        cache_key = (text, font, size, color)
        text_surf = self._text_cache.get(cache_key)
        if text_surf is None:
            font_obj = pygame.font.SysFont(font, size)
            text_surf = font_obj.render(text, True, color)
            self._text_cache[cache_key] = text_surf

        rect = text_surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        if not center:
            rect.topleft = (x, y)
        self.screen.blit(text_surf, rect)