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

        self.scenes = {}
        self.scene_solids = {}
        self.scene_objects = {}
        self.active_scene = None

    def run(self):
        self.keys_pressed = pygame.key.get_pressed()
        
        pygame.display.flip()
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        return True
    
    def scene(self, name):
        def scene_func(func):
            self.scenes[name] = func
            if name not in self.scene_solids:
                self.scene_solids[name] = []
            return func
        return scene_func
    
    @contextmanager
    def assets(self, scene_name):
        prev_scene = self.active_scene
        self.active_scene = scene_name

        if scene_name not in self.scene_solids:
            self.scene_solids[scene_name] = []
        if scene_name not in self.scene_objects:  
            self.scene_objects[scene_name] = []

        try:
            yield
        finally:
            self.active_scene = prev_scene

    def run_scene(self, name):
        if name in self.scenes:
            self.scenes[name]()
            self.active_scene = name
        else:
            print(f"Scene '{name}' not found!")
    
    

    def RenderText(self, Text, x, y,Font="TimesNewRoman", FontSize=14, color=(0,0,0)):
        font = pygame.font.SysFont(Font, FontSize)
        text = font.render(Text, False, color)
        self.screen.blit(text, (x,y))

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
