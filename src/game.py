import pygame, pytmx, pyscroll
from src.drawing import Draw
from src.logs_writer import *
from src.save_writer import *
from src.sprite import Sprite
from src.player import Player
from src.map_manager import Map_Manager
import time


class Game():
    def __init__(self)->None:
        #La fenêtre du jeu
        self.screen = pygame.display.set_mode((1000, 700), flags=pygame.RESIZABLE)
        pygame.display.set_caption("THE NCI GAME !")

        #Vitesse à laquelle le jeu va exécuter la boucle par seconde
        self.fps = 60

        #L'outil d'affichage, permet d'afficher ce qu'on veut sur le screen
        self.drawer = Draw(self.screen)

        #Gérer les différentes cartes
        self.map_manager = Map_Manager(self.screen)

        #Créer un joueur
        self.player = Player()









    def init_map_groups(self, which_enter:str|None="main_enter")->None:
        #Créer le groupe
        self.group = pyscroll.PyscrollGroup(self.map_manager.map_layer, default_layer=5)
        self.group.add(self.player)

        #Placer le joueur à sa position de départ
        object_for_player_pos = self.map_manager.tmx_data.get_object_by_name(which_enter)    #main_enter : nom du point de départ principal
        self.player.tp_sprite_to((object_for_player_pos.x,object_for_player_pos.y))

        #Obtenir (tempo) la collision de la sortie, optimal : for objetc by class with tmx
        self.group_exit_collides = []
        try:
            exit_est = self.map_manager.tmx_data.get_object_by_name("est_exit")  #
            self.group_exit_collides.append(("est_exit",pygame.Rect(exit_est.x,exit_est.y,exit_est.width,exit_est.height)))  #
        except KeyError:  #Error lorsque l'exit n'existe pas
            pass
        
        try:
            exit_ouest = self.map_manager.tmx_data.get_object_by_name("ouest_exit")  #
            self.group_exit_collides.append(("ouest_exit",pygame.Rect(exit_ouest.x,exit_ouest.y,exit_ouest.width,exit_ouest.height)))  #
        except KeyError:  #Error lorsque l'exit n'existe pas
            pass

        try:
            exit_nord = self.map_manager.tmx_data.get_object_by_name("nord_exit")  #
            self.group_exit_collides.append(("nord_exit",pygame.Rect(exit_nord.x,exit_nord.y,exit_nord.width,exit_nord.height)))  #
        except KeyError:  #Error lorsque l'exit n'existe pas
            pass

        try:
            exit_sud = self.map_manager.tmx_data.get_object_by_name("sud_exit")  #
            self.group_exit_collides.append(("sud_exit",pygame.Rect(exit_sud.x,exit_sud.y,exit_sud.width,exit_sud.height)))  #
        except KeyError:  #Error lorsque l'exit n'existe pas
            pass


        #Collisions
        self.collision_rects = []
        for obj_collision in self.map_manager.tmx_data.objects:
            if obj_collision.type == "collision":
                self.collision_rects.append(pygame.Rect(obj_collision.x,obj_collision.y,obj_collision.width,obj_collision.height))






#Récup tous les éléments relatifs au jeu en général, style quitter, menu ...
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

#Récup les input mais pr faire des actions avec le joueur
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

#Bouger les sprites en fonctions de leurs colisions
    def move_sprites(self)->None:
        self.player.move(self.fps)

#Mettre à jour les objets sur la carte
    def update_objects(self)->None:
        self.group.update()

        #Vérifications exit
        for exit_collision in self.group_exit_collides:
            if self.player.feet.colliderect(exit_collision[1]):   #Rect de l'exit
                exit_name = exit_collision[0]
                self.map_manager.switch_map(self.player,exit_name)
                self.init_map_groups(self.map_manager.cardinal_point_convert(exit_name))

        #Vérifications colisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_rects) > -1:
                sprite.move_back()         

#Afficher les updates
    def paint(self)->None:
        #Après que layer group ait été update
        self.group.draw(self.screen)
        self.drawer.draw_on_map()

#Bouger la caméra avec le joueur
    def update_camera(self)->None:
        self.group.center(self.player.pos)

#Retourner des infos de fonctionnement du jeu
    def get_stats_info_running(self)->None:
        self.true_fps = self.clock.get_fps()




























#Boucle du jeu
    def run(self)->None:
        self.init_map_groups()

        #Variable pour faire continuer ou non le jeu
        self.running = True
        #Clock pr les fps
        self.clock = pygame.time.Clock()

        #Boucle du jeu
        while self.running:
            #Touches
            self.catch_events()
            self.handle_player_inputs()

            #Events et forces
            self.move_sprites()
            self.update_objects()
            
            #Affichage
            self.paint()
            self.update_camera()
            
            #Running correctly
            self.get_stats_info_running()
            self.clock.tick(self.fps)
            