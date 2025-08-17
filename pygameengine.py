"""    ===== pygameengine.py =====    """
import pygame

pygame.init()

PYGAMEENGINE_VERSION = "V1.0"
APP_NAME_ENGINE_TAMPLATE = f" | Running with PyGameEngine {PYGAMEENGINE_VERSION}"

class PyGameEngine():

    def init(self, window_size = (500, 500), app_name = "Application", icon_path = None):
        self.screen = pygame.display.set_mode(window_size)

        pygame.display.set_caption(app_name + PYGAMEENGINE_VERSION)
        
        if icon_path:
            image_icon = pygame.image.load(icon_path).convert_alpha()
            pygame.display.set_icon(image_icon)
        
        self.m_clck = False
    
    def run(self):
        self.keys_pressed = pygame.key.get_pressed()
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        return True
        

    def RenderText(self, Text, x, y,Font="TimesNewRoman", FontSize=14, color=(0,0,0)):
        font = pygame.font.SysFont(Font, FontSize)
        text = font.render(Text, False, color)
        self.screen.blit(text, (x,y))

    def MouseClciked(self):
        pressed = False
        if not(self.m_clck) and pygame.mouse.get_pressed()[0]:
            self.m_clck = True
            pressed = True
        if not(pygame.mouse.get_pressed()[0]):
            self.m_clck = False
        return pressed
    
    def KeyPressed(self, key):
        return self.keys_pressed[key]

class Asset():
    def __init__(self,screen, img_path, Width = None, Height = None):
        self.surface = screen

        self.img = pygame.image.load(img_path).convert_alpha()
        if not Width:
            Width = self.img.get_width()
        if not Height:
            Height = self.img.get_height()
        
        self.img = pygame.transform.scale(self.img, (Width, Height))
    
    def draw(self, x, y):
        self.pos = (x, y)
        self.surface.blit(self.img, self.pos)
        self.rect = self.img.get_rect()

    def scale(self, W, H):
        self.img = pygame.transform.scale(self.img, (W, H))