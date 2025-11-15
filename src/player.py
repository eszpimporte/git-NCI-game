import pygame
from src.sprite import Sprite

class Player(Sprite):
    DEFAULT_PLAYER_SPEED = 300


    def __init__(self):
        super().__init__((320,100),'img/assets/sprites/personnage_base.png')
        self.movible = True
        self.speed = Player.DEFAULT_PLAYER_SPEED

        #zone et tronçon où se situe le player
        self.zone = "rouilny"
        self.troncon = (0,0)
        self.subzone = "None"


    def move_zone(self, zone:str, troncon:tuple[int], subzone:str|None="None")->None:
        self.zone = zone
        self.troncon = troncon
        self.subzone = subzone