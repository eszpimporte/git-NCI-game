import pygame, pytmx, pyscroll

class Draw():
    def __init__(self, screen:pygame.Surface)->None:
        self.screen = screen
    
    def draw_on_map(self)->None:

        #self.screen.blit(objet,(0,0))
        pygame.display.flip()