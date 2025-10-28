import pygame, math

class Sprite(pygame.sprite.Sprite):
    DEFAULT_SPRITE_SPEED = 50
    DEFAULT_SPRITE_COLORKEY = [255,255,255]


    def __init__(self, pos:tuple[int]|None=(0,0), fichier_imgae:str|None=None, movible:bool|None=False)->None:
        super().__init__()

        #Position
        self.pos = pos
        self.old_pos = self.pos[:]

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
        self.feet = pygame.Rect(0,0,self.rect.width*0.6,12)

    #Lier les coordonnées x et y avec la position du sprite
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
    def tp_sprite_to(self, pos):
        self.pos = pos
        self.update()
        self.feet.midbottom = self.rect.midbottom


    #Fonction appliquant tous les déplacements aux personnages qu'il est censé subir, cette fonction
    #est donc appelée dans game pour tous les sprites movibles
    def move(self, fps:int):
        if self.movible:
            vect_norme = math.sqrt(self.vect_x**2 + self.vect_y**2)
            
            if vect_norme != 0:
                #Obtenir avant déplacement l'ancienne colision
                self.old_pos = self.pos[:]
                #Bouger le sprite relativement à la vitesse, fps et mouvement
                self.x += self.vect_x*self.speed/(fps*vect_norme)
                self.y += self.vect_y*self.speed/(fps*vect_norme)
                #Bouger la colision au niveau des pieds
                self.update()
                self.feet.midbottom = self.rect.midbottom
                #NE PAS ACCUMULER LE MOUVEMENT (à part sys d'acceleration)
                self.vect_x = 0
                self.vect_y = 0
    

    #Se replacer si colision
    def move_back(self):
        self.pos = self.old_pos[:]
        self.feet.midbottom = self.rect.midbottom

    #Essentiel pr bouger le rect du sprite avec le sprite dn le code
    def update(self):
        self.rect.topleft = self.pos

    #Retourner l'image à afficher
    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.fichier_image_sprite, (0,0), (x,y,32,32))
        return image