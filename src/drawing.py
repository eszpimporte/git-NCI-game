import pygame, pytmx, pyscroll

class Draw():
    red = (200, 50, 50)
    black = (0,0,0)

    def __init__(self, screen:pygame.Surface)->None:
        self.screen = screen


        #assets à load
        self.mainfondlight = pygame.image.load("img/assets/background/mainfond.jpeg")
        self.bouton = pygame.image.load("img/assets/sprites/options/bouton.png")
        self.bouton.set_colorkey((255,255,255))
    
    def draw_on_screen(self, object_to_draw:pygame.Surface, coord:tuple[int], newsize:tuple[int]|None=None)->None:
        if newsize != None:
            object = pygame.transform.scale(object_to_draw, newsize)
        else:
            object = object_to_draw
        self.screen.blit(object, coord)

    def draw_on_screen_rect(self, object_to_draw:pygame.Surface, coord:tuple[int], rect_area:pygame.Rect, newsize:tuple[int]|None=None)->None:
        if newsize != None:
            object = pygame.transform.scale(object_to_draw, newsize)
        else:
            object = object_to_draw
        self.screen.blit(object, coord, rect_area)

    def draw_dark_on_screen(self, intensity:int):
        surface = pygame.Surface(self.screen.get_size())
        surface.set_alpha(255-intensity)
        self.screen.blit(surface,(0,0))
    
    def draw_text_on_screen(self, text:str, color:tuple[int], coord:tuple[int]):
        pass