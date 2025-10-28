import pygame, math

class Sprite(pygame.sprite.Sprite):
    DEFAULT_SPRITE_SPEED = 50
    DEFAULT_SPRITE_COLORKEY = [255,255,255]


    def __init__(self, pos:tuple[int]|None=(0,0), fichier_imgae:str|None=None, movible:bool|None=False)->None:
        super().__init__()
        #Position
        self.pos = pos

        #Deplacement
        self.movible = movible
        self.speed = Sprite.DEFAULT_SPRITE_SPEED
        self.vect_x = 0
        self.vect_y = 0
        self.total_vects = {}

        #Le fichier dans lequel y'a tous les sprites des animations
        self.fichier_image_sprite = pygame.image.load(fichier_imgae)

        #ces noms NE DOIVENT PAS être changés !!
        self.image = self.get_image(0,0)
        #La couleur de fond
        self.image.set_colorkey(Sprite.DEFAULT_SPRITE_COLORKEY)
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
    

    #Où le sprite est placé au lancement
    def init_position_at_start(self, pos):
        self.x = pos[0]
        self.y = pos[1]


    #Fonction appliquant tous les déplacements aux personnages qu'il est censé subir, cette fonction
    #est donc appelée dans game pour tous les sprites movibles
    def move(self, fps:int):
        if self.movible:
            vect_norme = math.sqrt(self.vect_x**2 + self.vect_y**2)
            
            if vect_norme != 0:
                self.x += self.vect_x*self.speed/(fps*vect_norme)
                self.y += self.vect_y*self.speed/(fps*vect_norme)

                self.vect_x = 0
                self.vect_y = 0


    def update(self):
        self.rect.topleft = self.pos


    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.fichier_image_sprite, (0,0), (x,y,32,32))
        return image