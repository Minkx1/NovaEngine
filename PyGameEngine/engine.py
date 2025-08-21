""" ===== engine.py ===== """

import pygame, threading,sys,subprocess

pygame.init()

# ========================
# ENGINE CONSTANTS
# ========================
PYGAMEENGINE_VERSION = "V1.5.0"
APP_NAME_ENGINE_TEMPLATE = f" | Running with PyGameEngine {PYGAMEENGINE_VERSION}"


class PyGameEngine:
    """
    A lightweight wrapper around PyGame to simplify game loop,
    input handling, and scene management.
    """

    # ========================
    # INITIALIZATION
    # ========================
    def init(self, window_size=(500, 500), app_name="Game", icon_path=None, fps=60):
        """Initialize the game window, clock, and base engine properties."""
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(app_name + APP_NAME_ENGINE_TEMPLATE)

        if icon_path:
            image_icon = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(image_icon)

        self.clock = pygame.time.Clock()
        self.keys_pressed = []
        self.m_clck = False
        self.fps = fps

        self.scenes = []
        self.active_scene = None
            
        self.main_run_func = self.run_active_scene

        self.threads = []
        self.cmd_allow = True

        return self

    # ========================
    # MAIN LOOP
    # ========================
    def run(self, main_globals=None):
        """Run the main game loop and threads."""
        self.console_vars = main_globals if main_globals else {}

        # Threads
        for thread in self.threads:
            def thread_loop():
                running = True
                while running:
                    # Call the main game logic provided by user
                    thread()
            threading.Thread(target=thread_loop, daemon=True).start()

        # Main Game Loop
        if self.cmd_allow:
            def run_cmd_input():
                while True:
                    cmd = input(">>> ")
                    if cmd == "kill()":
                        self.kill()
                        break
                    elif cmd == "restart()":
                        subprocess.Popen([sys.executable] + sys.argv)
                        self.kill()
                        break
                    try:
                        eval(cmd, getattr(self, "console_vars", {}))
                    except Exception as e:
                        print("Error:", e)
            threading.Thread(target=run_cmd_input, daemon=True).start()

        self.running = True
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()

            # Call the main game logic provided by user
            if self.main_run_func:
                self.main_run_func()

            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Update display and regulate FPS
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        sys.exit()
    
    def kill(self):
        self.running = False
    
    def run_active_scene(self):
        if self.active_scene:
            scene = self.active_scene
            scene.run()
    
    def set_active_scene(self, Scene):
        self.active_scene = Scene

    def main(self):
        """Decorator to register the main game function."""
        def decorator(func):
            self.main_run_func = func
            return func
        return decorator

    def thread(self):
        """Decorator to register threads."""
        def decorator(func):
            self.threads.append(func)
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
