import pygame, pytmx, pyscroll
from src.game import Game
from src.save_writer import init_save

if __name__ == '__main__':
    init_save()

    pygame.init()
    game = Game()
    game.run()

    pygame.quit()