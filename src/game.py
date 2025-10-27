import pygame, pytmx, pyscroll
from src.drawing import Draw
from src.logs_writer import *
from src.save_writer import *
import time


class Game():
    def __init__(self)->None:
        self.screen = pygame.display.set_mode((1000, 700), flags=pygame.RESIZABLE)
        pygame.display.set_caption("THE NCI GAME !")

        #Load les données -> à exporter
        tmx_data = pytmx.util_pygame.load_pygame("img/assets/cartes/map_rouilny_0_0.tmx")

        #Récupérer les données pour pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        #Les calques
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        self.layer_group = pyscroll.PyscrollGroup(map_layer, default_layer=0)


        #L'outil d'affichage
        self.drawer = Draw(self.screen)

        #Late attributs
        self.running = True


    def catch_events(self)->None:
        for event in pygame.event.get():
            #Keys
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_p:
                    #Mettre toutes les variables à save dans save
                    to_save()
                
            elif event.type == pygame.QUIT:
                self.running = False

    def paint(self)->None:
        self.layer_group.draw(self.screen)
        self.drawer.draw_on_map()

    def run(self)->None:
        self.running = True

        while self.running:
            self.catch_events()
            self.paint()
            