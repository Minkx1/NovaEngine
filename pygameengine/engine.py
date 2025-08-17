"""    ===== engine.py =====    """
import pygame

pygame.init()

PYGAMEENGINE_VERSION = "V1.2"
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

        self.solid_assets = []
    
    def run(self):
        self.keys_pressed = pygame.key.get_pressed()
        
        pygame.display.flip()
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        return True
        

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
