import pygame, pytmx, pyscroll

DEFAULT_FONT = "Arial"
class Draw():
    red = (200, 50, 50)
    black = (0,0,0)

    def __init__(self, screen:pygame.Surface)->None:
        self.screen = screen


        #assets à load
        self.mainfond = pygame.image.load("img/assets/background/mainfond.jpeg")
        self.bouton = pygame.image.load("img/assets/sprites/options/bouton.png").convert()
        self.bouton.set_colorkey((255,255,255))
        self.bouton_size = self.bouton.get_size()
    
    def draw_on_screen(self, object_to_draw:pygame.Surface, coord:tuple[float], newsize:tuple[float]|None=None)->None:
        if newsize != None:
            object = pygame.transform.scale(object_to_draw, newsize)
        else:
            object = object_to_draw
        self.screen.blit(object, coord)

    def draw_on_screen_rect(self, object_to_draw:pygame.Surface, coord:tuple[float], rect_area:pygame.Rect, newsize:tuple[float]|None=None)->None:
        if newsize != None:
            object = pygame.transform.scale(object_to_draw, newsize)
        else:
            object = object_to_draw
        self.screen.blit(object, coord, rect_area)

    def draw_dark_on_screen(self, intensity:int):
        surface = pygame.Surface(self.screen.get_size())
        surface.set_alpha(255-intensity)
        self.screen.blit(surface,(0,0))
    
    def draw_text_on_screen(self, text:str, color:tuple[int], coord:tuple[int], font:str=DEFAULT_FONT,txt_size:int=16,bold:bool=False, italic:bool=False):
        surface_text = pygame.font.SysFont(font,size=txt_size,bold=bold,italic=italic).render(text, False, color)
        self.screen.blit(surface_text, self.rel(surface_text.get_size(),coord=coord))
    
    def draw_text_on_screen_not_rel(self, text:str, color:tuple[int], coord:tuple[int], font:str=DEFAULT_FONT,txt_size:int=16,bold:bool=False, italic:bool=False):
        surface_text = pygame.font.SysFont(font,size=txt_size,bold=bold,italic=italic).render(text, False, color)
        self.screen.blit(surface_text, coord)
    
    #Renvoie les coordonnées relatives du centre par rap au centre sur le screen et entre 0 à 1
    def rel(self, size:tuple[float], x:float=0, y:float=0, coord:tuple[float]|None=None):
        if coord!=None :
            return coord[0]-size[0]/2,coord[1]-size[1]/2
        else:
            return (self.screen.get_width()*(1+x)-size[0])/2,(self.screen.get_height()*(1+y)-size[1])/2