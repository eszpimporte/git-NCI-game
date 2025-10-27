import pygame
from src.sprite import Sprite

class Player(Sprite):
    def __init__(self):
        super().__init__((320,100),'img/assets/sprites/personnage_base.png')