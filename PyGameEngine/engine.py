""" ===== engine.py ===== """

import pygame, threading,sys,subprocess, time
from typing import Tuple, Union
from enum import Enum

pygame.init()

# ========================
# ENGINE CONSTANTS
# ========================
PYGAMEENGINE_VERSION = "V1.5.0"
APP_NAME_ENGINE_TEMPLATE = f" | Running with PyGameEngine {PYGAMEENGINE_VERSION}"

# ========================
# BASIC COLORS 
# ========================
class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED   = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE  = (0, 0, 255)

class PyGameEngine:
    """
    A lightweight wrapper around PyGame to simplify game loop,
    input handling, and scene management.
    """

    # ========================
    # INITIALIZATION
    # ========================
    def __init__(self, window_size=(500, 500), app_name="Game", icon_path=None, fps=60, show_fps=False):
        """Initialize the game window, clock, and base engine properties."""
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(app_name + APP_NAME_ENGINE_TEMPLATE)

        if icon_path:
            image_icon = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(image_icon)

        self.clock = pygame.time.Clock()
        self.m_clck = False
        self.fps = fps
        self.show_fps = show_fps

        self.keys_pressed = []
        self.key_single_state = {}

        self.cooldowns = {}
        self.intervals = []
        
        self.scenes = []
        self.active_scene = None
        
        self.main_run_func = self.run_active_scene

        self.threads = []
        self.cmd_allow = True

    # ========================
    # MAIN LOOP
    # ========================
    def run(self, main_globals=None):
        """Run the main game loop and threads."""
        self.console_vars = main_globals if main_globals else {}

        # Command Input
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
        
        # Main Game Loop
        self.running = True
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()

            # Call the main game logic provided by user
            if self.main_run_func:
                self.main_run_func()

            #showing FPS
            if self.show_fps:
                fps = str(round(self.clock.get_fps(), 3))
                self.render_text(fps, 5, 5)

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update display and regulate FPS
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # self.quit()
    
    def quit(self):
        self.running = False
        print("[Engine] Quiting the game")
        import sys
        sys.exit()

    def main(self):
        """Decorator to register the main game function."""
        def decorator(func):
            self.main_run_func = func
            return func
        return decorator

    def new_thread(self):
        """Decorator to register threads."""
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
        """Run a specific scene if it's registered."""
        if scene in self.scenes:
            scene.run()
            self.active_scene = scene
        else:
            print("Scene not found!")
    
    def run_active_scene(self):
        if self.active_scene:
            scene = self.active_scene
            scene.run()
    
    def set_active_scene(self, Scene):
        self.active_scene = Scene
    
    # ========================
    # INPUT MANAGEMENT
    # ========================

    def MouseClicked(self, button=0):
        """
        Detects a single mouse click (not hold).
        Returns True only when the mouse button is first pressed.
        """
        pressed = False
        if not self.m_clck and pygame.mouse.get_pressed()[button]:
            self.m_clck = True
            pressed = True
        if not pygame.mouse.get_pressed()[button]:
            self.m_clck = False
        return pressed
    
    def KeyPressed(self, key):
        """
        Check if a specific key is currently pressed.

        Args:
            key (int): pygame key constant, e.g. pygame.K_w

        Returns:
            bool: True if the key is pressed, False otherwise
        """

        try:
            pressed = bool(self.keys_pressed[key])
        except (IndexError, TypeError):
            return False

        if pressed:
            if not self.key_single_state.get(key, False):
                # вперше натиснули
                self.key_single_state[key] = True
                return True
            else:
                # утримується
                return False
        else:
            # клавіша відпущена
            self.key_single_state[key] = False
            return False
    
    def KeyHold(self, key):
        """
        Check if a specific key is currently hold.

        Args:
            key (int): pygame key constant, e.g. pygame.K_w

        Returns:
            bool: True if the key is hold, False otherwise
        """
        try:
            pressed = bool(self.keys_pressed[key])
        except (IndexError, TypeError):
            return False
        
        return pressed
    
    # ========================
    # TIME MANAGEMENT
    # ========================

    def Timer(self, duration):
        """Decorator, that runs function adter $duration$ seconds"""
        def decorator(func):
            threading.Timer(duration, func).start()
            return func
        return decorator
    
    def Cooldown(self, key, duration, force=False):
        if self.cooldowns.get(key) == None or force:
            @self.new_thread()
            def _():
                self.cooldowns[key] = False 
                time.sleep(duration)
                self.cooldowns[key] = True

        return self.cooldowns.get(key, False)

    
    # ========================
    # UTILITIES
    # ========================

    def fill_background(self,color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK, image: pygame.Surface = None):
        """
        Fill the background with a color or an image.

        Args:
            color: background color
            image: optional pygame.Surface to use as background
        """
        screen = self.screen
        if image:
            screen.blit(image, (0, 0))
        else:
            if isinstance(color, Colors):
                color = color.value
            screen.fill(color)
    
    def render_text(
        self,text: str,
        x: float, y: float,
        font: str = "TimesNewRoman", size: int = 14,
        color: Union[Colors, Tuple[int, int, int]] = Colors.BLACK,
        center: bool = False
    ):
        """
        Render text on the screen at (x, y).

        Args:
            text: string to render
            x, y: coordinates
            font: font name
            size: font size
            color: text color (Colors enum or RGB tuple)
            center: if True, center the text at (x, y)
        """
        screen = self.screen
        
        if isinstance(color, Colors):
            color = color.value
        
        font_obj = pygame.font.SysFont(font, size)
        text_surf = font_obj.render(text, True, color)

        rect = text_surf.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)

        screen.blit(text_surf, rect)