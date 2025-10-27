import pygame

class Sprite():
    def __init__(self, name:str, pos:tuple[int], image, movible:bool|None=False, animation:bool|None=False, colision:bool|None=True ,dialogue:dict|None={True:False}, player:bool|None=False)->None:
        #Nom du personnage qu'on peut afficher
        self.name = name
        #Position x,y,z
        self.pos = pos
        #Dossier des images pour le sprite, s'il est animable, toutes les frames seront rangées là
        self.image = image
        #Si movible
        self.movible = movible
        #Si animable
        self.animation = animation
        #Si agir comme une colision
        self.colision = colision
        #Toutes les données du dialogue
        self.dialogue = dialogue
        #Si c'est le player
        self.player = player
    
    #Toutes les property de position
    @property
    def x(self):
        return self.pos[0]
    @x.setter
    def x_setter(self):
        self.pos[0] = self.x
    
    @property
    def y(self):
        return self.pos[1]
    @y.setter
    def y_setter(self):
        self.pos[1] = self.y
    
