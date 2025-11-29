from src.drawing import Draw
import pygame


class Bouton():
    last_return = ""
    actives_boutons = []

    def __init__(self, screen:pygame.Surface, rect:pygame.Rect, text:str, return_text:str):
        self.screen = screen
        self.rect = rect
        self.text = text
        self.return_text = return_text

        self.drawer = Draw(self.screen)

        Bouton.actives_boutons.append(self)

    @property
    def coord(self):
        return (self.rect.x,self.rect.y)
    @coord.setter
    def coord(self, value:tuple[int]):
        self.rect.x = value[0]
        self.rect.y = value[1]
    
    @property
    def size(self):
        return (self.rect.width, self.rect.height)
    @size.setter
    def size(self, value:tuple[int]):
        self.rect.height = value[0]
        self.rect.width = value[1]

    @property
    def height(self):
        return self.size[1]
    @height.setter
    def height(self, value):
        self.size = (self.size[0], value)
    
    @property
    def width(self):
        return self.size[0]
    @width.setter
    def height(self, value):
        self.size = (value, self.size[1])

    @property
    def x(self):
        return self.coord[0]
    @x.setter
    def x(self, value):
        self.coord = (value, self.coord[1])
    
    @property
    def y(self):
        return self.coord[1]
    @y.setter
    def y(self, value):
        self.coord = (self.coord[0], value)

    @property
    def center(self):
        return (self.x+self.width/2,self.y+self.height/2)


    @classmethod
    def active_all():
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        button : Bouton
        for button in Bouton.actives_boutons:
            if (button.y < mouse_pos[1] and mouse_pos[1] < button.y+button.height) and (button.x < mouse_pos[0] and mouse_pos[0] < button.x+button.width):
                if mouse_pressed:
                    Bouton.last_return = button.return_text
                button.drawer.draw_text_on_screen(button.text, Draw.red, button.center)
            else:
                button.drawer.draw_text_on_screen(button.text, Draw.black, button.center)
    
    @classmethod
    def erased():
        for button in Bouton.actives_boutons:
            del button
        Bouton.actives_boutons = []
