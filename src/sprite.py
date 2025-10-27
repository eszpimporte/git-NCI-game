import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos:tuple[int]|None=(0,0),fichier_imgae:str|None=None)->None:
        super().__init__()
        #Position
        self.pos = pos

        #Le fichier dans lequel y'a tous les sprites des animations
        self.fichier_image_sprite = pygame.image.load(fichier_imgae)

        #ces noms NE DOIVENT PAS être changés !!
        self.image = self.get_image(0,0)
        #La couleur de fond
        self.image.set_colorkey([255,255,255])
        #Pour créer un rect ... en gros on en a besoin
        self.rect = self.image.get_rect()


    @property
    def x(self):
        return self.pos[0]
    @x.setter
    def x(self, value):
        self.pos = (value,self.y)
    @property
    def y(self):
        return self.pos[1]
    @y.setter
    def y(self, value):
        self.pos = (self.x,value)
    

    def update(self):
        self.rect.topleft = self.pos


    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.fichier_image_sprite, (0,0), (x,y,32,32))
        return image