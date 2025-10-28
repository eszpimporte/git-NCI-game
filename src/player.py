import pygame
from src.sprite import Sprite

class Player(Sprite):
    DEFAULT_PLAYER_SPEED = 100


    def __init__(self):
        super().__init__((320,100),'img/assets/sprites/personnage_base.png')
        self.movible = True
        self.speed = Player.DEFAULT_PLAYER_SPEED