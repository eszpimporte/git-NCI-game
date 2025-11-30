from src.drawing import Draw
import pygame


class Bouton():
    last_return = ""
    actives_boutons = []

    def __init__(self, screen:pygame.Surface, coord_rel:tuple[int], size:tuple[int], text:str, return_text:str, code:int=0, txt_size:int=16):
        self.screen = screen
        self.coord_rel = coord_rel
        self.size = size
        self.text = text
        self.return_text = return_text
        self.code = code
        self.txt_size = txt_size

        self.drawer = Draw(self.screen)

        Bouton.actives_boutons.append(self)

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
    def width(self, value):
        self.size = (value, self.size[1])

    @property
    def coord(self):
        return self.drawer.rel(self.drawer.bouton.get_size(),self.coord_rel[0],self.coord_rel[1])

    @property
    def x(self):
        return self.coord[0]
    
    @property
    def y(self):
        return self.coord[1]

    @property
    def center(self):
        return (self.x+self.width/2,self.y+self.height/2)


    @classmethod
    def active_all(cls, code:int, can_press_again:bool):
        mouse_pressed = pygame.mouse.get_pressed()[0] and can_press_again
        mouse_pos = pygame.mouse.get_pos()
        button : Bouton
        for button in Bouton.actives_boutons:
            if button.code == code:
                button.drawer.draw_on_screen(button.drawer.bouton,button.coord,button.size)
                if (button.y < mouse_pos[1] and mouse_pos[1] < button.y+button.height) and (button.x < mouse_pos[0] and mouse_pos[0] < button.x+button.width):
                    if mouse_pressed:
                        Bouton.last_return = button.return_text
                    button.drawer.draw_text_on_screen(button.text, Draw.red, button.center, txt_size=button.txt_size)
                else:
                    button.drawer.draw_text_on_screen(button.text, Draw.black, button.center, txt_size=button.txt_size)
        return mouse_pressed
        
    @classmethod
    def erased(cls, erase_range:list):
        button : Bouton
        copie_liste_bouton = Bouton.actives_boutons.copy()
        for button in copie_liste_bouton:
            if button.code in erase_range:
                Bouton.actives_boutons.remove(button)
                del button