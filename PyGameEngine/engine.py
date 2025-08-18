""" ===== engine.py ===== """

import pygame

pygame.init()

# ========================
# ENGINE CONSTANTS
# ========================
PYGAMEENGINE_VERSION = "V1.4.0"
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
        self.main_run_func = None

    # ========================
    # MAIN LOOP
    # ========================
    def run(self):
        """Run the main game loop."""
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

    def main(self):
        """Decorator to register the main game function."""
        def decorator(func):
            self.main_run_func = func
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

    # ========================
    # INPUT HELPERS
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
        """Check if a specific key is currently pressed."""
        return self.keys_pressed[key]
