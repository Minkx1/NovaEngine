"""===== engine.py ====="""

import pygame
import threading
from .dev_tools import log, get_globals

# ========================
# ENGINE CONSTANTS
# ========================
ENGINE_VERSION = "V1.9.0"
APP_NAME_ENGINE_TEMPLATE = f" | Running with NovaEngine {ENGINE_VERSION}"


# ========================
# MAIN INSTANCE CLASS
# ========================
class NovaEngine:
    """
    Lightweight PyGame framework for:
    - game loop, system inputs
    - input handling
    - scenes
    - timers & threads
    - text rendering
    """

    Engine = None

    # ========================
    # INITIALIZATION
    # ========================
    def __init__(self, window_size=(500, 500), app_name="Game", icon_path=None, fps=60):
        """
        Initialize the engine window and core systems.
        """

        pygame.init()

        self.app_name = app_name
        self.icon_path = icon_path

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(self.app_name + APP_NAME_ENGINE_TEMPLATE)

        if self.icon_path:
            pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())

        self.clock = pygame.time.Clock()
        self.fps = fps
        self.time = 0
        self.in_game_time = 0
        self.time_spent_frozed = 0
        self.time_froze = False

        self.debug = False
        self.dt: int = 0

        self.event_handlers = []

        # Input states
        self.m_clck = False
        self.mouse_clicked = False
        self.keys_pressed = []
        self.key_single_state = {}

        # Internal caches
        self._text_cache = {}
        self.cooldowns = []
        self.intervals = []

        # Scene system
        self.scenes = []
        self.active_scene = None
        self.main_run_func = None

        @self.main()
        def _():
            from .utils import Colors, Utils

            Utils.fill_background(Colors.WHITE)
            if self.active_scene: self.active_scene.run()

        self.globals = None

        # Threads
        self.threads = []
        self.terminal_allow = True
        self.running = False

        NovaEngine.Engine = self

    # ========================
    # MAIN LOOP
    # ========================

    def run(self, first_scene=None, save_manager=None):
        """Run the main game loop and optional command input thread."""
        self.globals = get_globals()

        # Start command input thread

        if self.terminal_allow:
            import sys
            import subprocess

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
                            creationflags=subprocess.CREATE_NEW_CONSOLE,  # new console
                        )
                        self.quit()
                        break
                    else:
                        try:
                            exec(cmd, getattr(self, "globals", {}))
                        except Exception as e:
                            log(e, error=True)

        # Working with first scene

        if first_scene is not None:
            try:
                self.active_scene = first_scene
            except Exception as e:
                log(f"{e}", sender="SceneManager", error=True)

        if not self.active_scene and self.scenes:
            self.active_scene = self.scenes[0]

        # Loading data from save

        if save_manager is not None:
            save_manager.load()

        # Game loop

        self.running = True
        while self.running:
            # base functional
            self.keys_pressed = pygame.key.get_pressed()
            self.mouse_clicked = self.MouseClicked(first_iter=True)
            self.time = pygame.time.get_ticks()
            if not self.time_froze:
                self.in_game_time = self.time - self.time_spent_frozed

            if self.main_run_func:
                self.main_run_func()

            if self.debug:
                from .utils import Utils
                Utils.render_text(
                    f"{round(self.clock.get_fps(), 2)}", 20, 20, center=True
                )
                Utils.render_text(
                    str(pygame.mouse.get_pos()),
                    *pygame.mouse.get_pos(),
                    size=10,
                    center=True,
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()                
                for handler in self.event_handlers:
                    handler.handle_event(event)

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000

        # Saving data to save

        if save_manager is not None:
            save_manager.save()

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
