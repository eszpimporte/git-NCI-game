import pygame, pytmx, pyscroll
from src.game import Game
from src.save_writer import Save

if __name__ == '__main__':
    pygame.init()

    #Save.choice_save()
    run = True
    while run:
        game = Game()
        run = game.run()

    pygame.quit()