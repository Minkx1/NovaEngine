"""===== engine.py ====="""

import pygame
import threading
import sys, os
import subprocess
import zipfile
import time
import inspect
from typing import Tuple, Union

pygame.init()

# ========================
# ENGINE CONSTANTS
# ========================
ENGINE_VERSION = "V1.7.0"
APP_NAME_ENGINE_TEMPLATE = f" | Running with NovaEngine {ENGINE_VERSION}"


def log(msg: str, sender="NovaEngine", error=False):
    """
    Log a message to console.

    Args:
        msg (str): The message to log.
        sender (str): The sender's name (default "NovaEngine").
        error (bool): If True, prefixes with 'Error:'.
    """
    prefix = f"[{sender}]"
    if error:
        print(f"{prefix} Error: {msg}")
    else:
        print(f"{prefix} {msg}")


def get_globals() -> dict:
    """
    Return the global variables of the script that started the call chain (script __main__).
    Works even if called inside a method of a class or engine.
    """
    frame = inspect.currentframe()
    while frame:
        globs = frame.f_globals
        if globs.get("__name__") == "__main__":
            return globs
        frame = frame.f_back
    return {}


class DevTools:
    """
    Developer utilities for packaging and testing.
    """

    @staticmethod
    def build_exe(
        main_file="main.py",
        name="game",
        icon_path="",
        onefile=True,
        noconsole=False,
        dist_path: str = None,
    ):
        """
        Build a Windows executable from a Python script using PyInstaller.

        Args:
            main_file (str): Path to the entry Python file.
            name (str): Name of the output exe.
            icon_path (str): Path to an icon file (*.ico).
            onefile (bool): Build as a single exe or as a folder.
            noconsole (bool): Hide console (GUI apps only).
            dist_path (str): Output directory (default = 'dist/').

        Notes:
            - Requires: pip install pyinstaller
            - Antivirus may give false positives.
            - Best used inside a clean venv.
        """
        flags = ["pyinstaller", f"--name={name}"]

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
            log("Running: " + " ".join(flags), sender="DevTools")
            subprocess.run(flags, check=True)
            out_dir = dist_path or "dist"
            log(
                f"✅ Build complete! File saved in '{out_dir}/{name}.exe'",
                sender="DevTools",
            )
        except subprocess.CalledProcessError as e:
            log(f"❌ Build failed: {e}", error=True, sender="DevTools")

    @staticmethod
    def build_archive(
        main_file="main.py",
        name="game",
        icon_path: str = None,
        onefile=True,
        noconsole=False,
        dist_path=None,
        sprite_dir="sprites",
        archive_dist="releases",
        archive_name: str = None,
    ):
        """
        Build exe and pack it with asset folder into a .zip archive.

        Args:
            main_file (str): entry file for PyInstaller
            name (str): exe name
            sprite_dir (str): folder with sprites/assets
            archive_dist (str): where to save archive (default = releases/)
            archive_name (str): name of archive (default = <name>.zip)
        """
        # 1. Спочатку збираємо exe
        DevTools.build_exe(
            main_file=main_file,
            name=name,
            icon_path=icon_path,
            onefile=onefile,
            noconsole=noconsole,
            dist_path=dist_path,
        )

        exe_path = os.path.join(dist_path or "dist", f"{name}.exe")
        if not os.path.exists(exe_path):
            log(f"❌ EXE not found at {exe_path}", error=True, sender="DevTools")
            return

        # 2. Готуємо архів
        os.makedirs(archive_dist, exist_ok=True)
        archive_name = archive_name or f"{name}.zip"
        archive_path = os.path.join(archive_dist, archive_name)

        try:
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Додаємо exe
                zipf.write(exe_path, arcname=os.path.basename(exe_path))

                # Додаємо папку з ассетами
                if os.path.isdir(sprite_dir):
                    for root, _, files in os.walk(sprite_dir):
                        for file in files:
                            filepath = os.path.join(root, file)
                            arcpath = os.path.relpath(
                                filepath, start=os.path.dirname(sprite_dir)
                            )
                            zipf.write(filepath, arcname=arcpath)

            log(f"✅ Archive built: {archive_path}", sender="DevTools")

        except Exception as e:
            log(f"❌ Archive build failed: {e}", error=True, sender="DevTools")


# ========================
# BASIC COLORS
# ========================
class Colors:
    """Predefined RGB colors."""

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class NovaEngine:
    """
    Lightweight PyGame framework for:
    - game loop, system inputs
    - input handling
    - scenes
    - timers & threads
    - text rendering
    """

    # ========================
    # INITIALIZATION
    # ========================
    def __init__(
        self,
        window_size=(500, 500),
        app_name="Game",
        icon_path=None,
        fps=60,
        enable_fullscreen=False,
    ):
        """
        Initialize the engine window and core systems.
        """
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
        self.dt: int = 0

        self.event_handlers = []

        # Input states
        self.m_clck = False
        self.mouse_clicked = False
        self.keys_pressed = []
        self.key_single_state = {}

        # Internal caches
        self._text_cache = {}
        self.cooldowns = {}
        self.intervals = []

        # Scene system
        self.scenes = []
        self.active_scene = None
        self.main_run_func = None

        @self.main()
        def _():
            self.fill_background(Colors.WHITE)
            self.run_active_scene()

        self.globals = None

        # Threads
        self.threads = []
        self.terminal_allow = True
        self.running = False

    # ========================
    # MAIN LOOP
    # ========================

    def run(self, first_scene=None):
        """Run the main game loop and optional command input thread."""
        self.globals = get_globals()

        # Start command input thread
        if self.terminal_allow:
            @self.new_thread()
            def run_cmd_input():
                while True:
                    cmd = input(">>> ")
                    if cmd == "kill()":
                        self.quit()
                        break
                    elif cmd == "restart()":
                        subprocess.Popen(
                            [sys.executable] + sys.argv,
                            creationflags=subprocess.CREATE_NEW_CONSOLE  # new console
                        )
                        self.quit()
                        break
                    else:
                        try:
                            exec(cmd, getattr(self, "globals", {}))
                        except Exception as e:
                            log(e, error=True)

        # Game loop

        if first_scene is not None:
            try:
                self.set_active_scene(first_scene)
            except Exception as e:
                log(f"{e}", "SceneManager", True)
        
        if not self.active_scene and self.scenes:
            self.active_scene = self.scenes[0]

        self.running = True
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()
            self.mouse_clicked = self.MouseClicked(first_iter=True)

            if self.main_run_func:
                self.main_run_func()

            if self.debug:
                self.render_text(
                    f"{round(self.clock.get_fps(), 2)}", 20, 20, center=True
                )
                self.render_text(
                    str(pygame.mouse.get_pos()),
                    *pygame.mouse.get_pos(),
                    size=10,
                    center=True,
                )

            if self.KeyPressed(pygame.K_F11) and self.enable_fullscreen:
                if self.fullscreen:
                    pygame.display.set_mode(self.screen.get_size())
                else:
                    pygame.display.set_mode(self.screen.get_size(), pygame.FULLSCREEN)
                self.fullscreen = not self.fullscreen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                for handler in self.event_handlers:
                    handler.handle_event(event)

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000

    def quit(self):
        """Stop engine and exit program."""
        self.running = False
        log("Quitting the game...")
        sys.exit()

    def main(self):
        """Decorator to register main game logic."""

        def decorator(func):
            self.main_run_func = func
            return func

        return decorator

    def new_thread(self):
        """Decorator to run function in a separate daemon thread."""

        def decorator(func):
            if func not in self.threads:
                self.threads.append(func)
                threading.Thread(target=func, daemon=True).start()
            return func

        return decorator

    def set_debug(self, value=True):
        """Enable or disable debug rendering (FPS, mouse pos)."""
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
        """Run the currently active scene."""
        if self.active_scene:
            self.active_scene.run()

    def set_active_scene(self, scene):
        """Set active scene without running it immediately."""
        self.active_scene = scene

    # ========================
    # INPUT MANAGEMENT
    # ========================
    def MouseClicked(self, button=0, first_iter=False):
        """Return True only on first mouse click (not hold)."""
        if not first_iter:
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
        """Return True while key is held down."""
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

    def Cooldown(self, key, duration, start=False):
        """Check or create a cooldown for a key."""
        if start:

            @self.new_thread()
            def _():
                self.cooldowns[key] = False
                time.sleep(duration)
                self.cooldowns[key] = True

        return self.cooldowns.get(key, True)

    def Interval(self, count, cooldown):
        """Call function `count` times with delay `cooldown` seconds (use -1 for infinite)."""

        def decorator(func):
            @self.new_thread()
            def cycle():
                if count == -1:
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
    def fill_background(
        self,
        color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK,
        image: pygame.Surface = None,
    ):
        """Fill the screen with a color or an image."""
        if image:
            self.screen.blit(image, (0, 0))
        else:
            if isinstance(color, Colors):
                color = color.value
            self.screen.fill(color)

    def render_text(
        self,
        text: str,
        x: float,
        y: float,
        font: str = "TimesNewRoman",
        size: int = 14,
        color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK,
        center: bool = False,
    ):
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

        self.screen.blit(text_surf, rect)
        return rect
