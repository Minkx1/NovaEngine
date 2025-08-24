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

def log(msg,sender="SparkEngine", error=False):
    if error:
        print(f"[{sender}] Error: {msg}")
    else:
        print(f"[{sender}] {msg}")

class DevTools:
    def build_exe(main_file="main.py", name="game", icon_path="", onefile=True, noconsole=False, dist_path:str =None):
        """
        Build a Windows executable from a Python script using PyInstaller.
        
        Parameters:
            main_file (str): Path to the main Python file (entry point) e.g. main.py
            name (str): Name of the output exe file (default = 'game').
            icon (str): Path to an icon file (*.ico) for the exe.
            onefile (bool): If True, build a single-file exe. If False, create a folder with dependencies.
            noconsole (bool): If True, disable the console window (for GUI apps).
            dist_path (str): Directory where the built exe will be stored (default = 'dist/').

        Notes:
            - Make sure PyInstaller is installed: pip install pyinstaller
            - Disable antivirus before building, as some AV may detect false positives.
            - Run this script from a clean virtual environment to avoid bundling unnecessary packages.
        """

        flags = [
            "pyinstaller",
            f"--name={name}"
        ]
        
        if onefile:
            flags.append("--onefile")
        if noconsole:
            flags.append("--noconsole")
        if icon_path:
            flags.append(f"--icon={icon_path}")
        if dist_path:
            flags.append(f"--distpath={dist_path}")
        
        flags.append(main_file)
        try:
            log(sender="DevTools",msg="Building EXE file: ".join(flags))
            subprocess.run(flags, check=True)
            log(f"✅ Build complete! File saved in '{dist_path}/{name}.exe'", sender="DevTools")
        except subprocess.CalledProcessError as e:
            log(f"❌ Build failed: {e}", error=True, sender="DevTools")

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
    def __init__(self, window_size=(500, 500), app_name="Game", icon_path=None, fps=60, enable_fullscreen=False):
        """Initialize game window, clock, engine state."""
        self.app_name = app_name
        self.icon_path = icon_path

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.app_name + APP_NAME_ENGINE_TEMPLATE)

        if self.icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.debug = False
        self.enable_fullscreen = enable_fullscreen
        self.fullscreen = False

        self.m_clck = False
        self.mouse_clicked = False
        self.keys_pressed = []
        self.key_single_state = {}

        self._text_cache = {}
        self.cooldowns = {}
        self.intervals = []

        self.scenes = []
        self.active_scene = None
        self.main_run_func = self.run_active_scene
        self.globals = None

        self.threads = []
        self.cmd_allow = True
        self.running = False

    # ========================
    # MAIN LOOP
    # ========================
    def run(self):
        """Run the main game loop and optional command input thread."""
        import inspect
        caller_frame = inspect.currentframe().f_back
        self.globals = caller_frame.f_globals

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
                        exec(cmd, getattr(self, "globals", {}))
                    except Exception as e:
                        log(e, error=True)

        self.running = True
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()
            self.mouse_clicked = self.MouseClicked(first_itter=True)

            # Execute main user logic
            if self.main_run_func: self.main_run_func()

            # Show FPS
            if self.debug: 
                self.render_text(f"{round(self.clock.get_fps(), 2)}", 5, 5)
                self.render_text(f"{pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]}", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], size=10,center=True)

            if self.KeyPressed(pygame.K_F11) and self.enable_fullscreen: 
                if self.fullscreen:
                    pygame.display.set_mode(self.screen.get_size())
                else:
                    pygame.display.set_mode(self.screen.get_size(), pygame.FULLSCREEN)

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def quit(self):
        """Stop engine and exit program."""
        self.running = False
        log("Quitting the game...")

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
    
    def set_debug(self, value=False):
        self.debug = value
        return self

    # ========================
    # SCENE MANAGEMENT
    # ========================
    def run_scene(self, scene):
        """Run a specific registered scene."""
        if scene in self.scenes:
            self.active_scene = scene
            scene.run()
        else:
            log("Scene not found!", error=True)

    def run_active_scene(self):
        if self.active_scene:
            self.active_scene.run()

    def set_active_scene(self, scene):
        self.active_scene = scene

    # ========================
    # INPUT MANAGEMENT
    # ========================
    def MouseClicked(self, button=0, first_itter=False):
        if not first_itter:
            """Return True only on first mouse click (not hold)."""
            pressed = False
            if not self.m_clck and pygame.mouse.get_pressed()[button]:
                self.m_clck = True
                pressed = True
            if not pygame.mouse.get_pressed()[button]:
                self.m_clck = False
            return pressed
        else:
            return self.mouse_clicked

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
    def Interval(self, count, cooldown):
        """
        Calls func $count$ times with delay $cooldown$ seconds.
        """
        def decorator(func):    
            @self.new_thread()
            def cycle():
                if count==-1:
                    while True:
                        func()
                        time.sleep(cooldown)
                else:
                    for _ in range(count):
                        func()
                        time.sleep(cooldown)
            return func
        return decorator

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