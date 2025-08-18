"""    ===== engine.py =====    """
import pygame
from contextlib import contextmanager

pygame.init()

PYGAMEENGINE_VERSION = "V1.3"
APP_NAME_ENGINE_TAMPLATE = f" | Running with PyGameEngine {PYGAMEENGINE_VERSION}"

class PyGameEngine():

    def init(self, window_size = (500, 500), app_name = "Game", icon_path = None, fps = 60):
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption(app_name + APP_NAME_ENGINE_TAMPLATE)
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

    def run(self):
        self.running = True

        while self.running:
            self.keys_pressed = pygame.key.get_pressed()
            
            self.main_run_func()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()
            self.clock.tick(self.fps)    
    
    
    def main(self):
        def decorator(func):
            self.main_run_func = func
            return func
        return decorator


    def run_scene(self, Scene):
        if Scene in self.scenes:
            Scene.run()
            self.active_scene = Scene
            # print(self.active_scene)
        else:
            print(f"Scene not found!")

    # ========================
    # INPUT HELPERS
    # ========================
    
    def MouseClicked(self, button = 0):
        pressed = False
        if not(self.m_clck) and pygame.mouse.get_pressed()[button]:
            self.m_clck = True
            pressed = True
        if not(pygame.mouse.get_pressed()[button]):
            self.m_clck = False
        return pressed
    
    def KeyPressed(self, key):
        return self.keys_pressed[key]
