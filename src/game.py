import pygame, pytmx, pyscroll
from src.drawing import Draw
from src.logs_writer import *
from src.save_writer import *
from src.sprite import Sprite
from src.player import Player
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
        map_layer.zoom = 1.5

        #Créer un joueur
        player_pos = tmx_data.get_object_by_name("first_start")
        self.player = Player()
        self.player.x = player_pos.x
        self.player.y = player_pos.y

        #Créer le groupe
        self.layer_group = pyscroll.PyscrollGroup(map_layer, default_layer=10)
        self.layer_group.add(self.player)

        #L'outil d'affichage
        self.drawer = Draw(self.screen)


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
        self.layer_group.update()
        self.layer_group.draw(self.screen)
        self.drawer.draw_on_map()

    
    def update_camera(self)->None:
        self.layer_group.center(self.player.pos)


    def run(self)->None:
        self.running = True

        while self.running:
            self.catch_events()
            self.paint()
            self.update_camera()
            