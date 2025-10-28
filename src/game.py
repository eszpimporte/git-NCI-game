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

        #Vitesse à laquelle le jeu va exécuter la boucle par seconde
        self.fps = 60

        #Load les données -> à exporter
        tmx_data = pytmx.util_pygame.load_pygame("img/assets/cartes/map_rouilny_0_0.tmx")
        #Récupérer les données pour pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)
        #Les calques
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1.5

        #Créer un joueur
        self.player = Player()
        object_for_player_pos = tmx_data.get_object_by_name("first_start")
        self.player.init_position_at_start((object_for_player_pos.x,object_for_player_pos.y))

        #Créer le groupe
        self.layer_group = pyscroll.PyscrollGroup(map_layer, default_layer=10)
        self.layer_group.add(self.player)

        #L'outil d'affichage
        self.drawer = Draw(self.screen)
    

    def handle_player_inputs(self)->None:
        input_pressed = pygame.key.get_pressed()

        if input_pressed[pygame.K_z]:
            self.player.vect_y -= 1
        if input_pressed[pygame.K_q]:
            self.player.vect_x -= 1
        if input_pressed[pygame.K_s]:
            self.player.vect_y += 1
        if input_pressed[pygame.K_d]:
            self.player.vect_x += 1


    def move_sprites(self)->None:
        self.player.move(self.fps)


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

    
    def get_stats_info_running(self)->None:
        self.true_fps = self.clock.get_fps()


    def run(self)->None:
        self.running = True
        self.clock = pygame.time.Clock()

        while self.running:
            #Touches
            self.catch_events()
            self.handle_player_inputs()

            #Events et forces
            self.move_sprites()
            
            #Affichage
            self.paint()
            self.update_camera()
            
            #Running correctly
            self.get_stats_info_running()
            self.clock.tick(self.fps)
            