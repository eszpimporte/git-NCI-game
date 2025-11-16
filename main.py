import pygame, pytmx, pyscroll
from src.game import Game
from src.save_writer import Save

if __name__ == '__main__':
    Save.choice_save()

    pygame.init()
    game = Game()
    game.run()

    pygame.quit()