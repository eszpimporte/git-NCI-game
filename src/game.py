import pygame, pytmx, pyscroll
from src.drawing import Draw
from src.logs_writer import *
from src.save_writer import Save
from src.sprite import Sprite
from src.player import Player
from src.map_manager import Map_Manager
from src.bouton import Bouton
import time


class Game():
    def __init__(self)->None:
        #Taille de l'écrant ingame
        self.SCREEN_DEFAULT_SIZE = (1000, 700)
        self.resize_by_hor = True

        #La fenêtre du jeu
        self.screen = pygame.display.set_mode(self.SCREEN_DEFAULT_SIZE, flags=pygame.RESIZABLE)
        pygame.display.set_caption("THE NCI GAME !")

        #Vitesse à laquelle le jeu va exécuter la boucle par seconde, init temp à 60
        self.fps = 60
        self.SEUIL_FPS = 20

        #L'outil d'affichage, permet d'afficher ce qu'on veut sur le screen
        self.drawer = Draw(self.screen)

        #Créer un joueur
        self.player = Player()



#FONCTIONS INITIATRICES DU JEU
#Fonctions pour charger la sauvegarde
    def load_save(self):
        self.NEW_SAVE = True
        save = Save.get_save()

        if len(save.keys()) != 0:
            self.NEW_SAVE = False
            #Init du player
            self.player.load_save(save["player"])

#Initialise tous les éléments de la carte
    def init_map_groups(self)->None:
        #Gérer les différentes cartes
        self.map_manager = Map_Manager(self.screen, self.player)
        if self.NEW_SAVE:
            self.load_groups_at_enter("main_enter")
        else:
            self.reload_groups()
        




#FONCTIONS DES MENUS
#Boucle du main menu
    def start_menu(self):
        #Variables
        self.start_menu_active = False
        self.running_start_menu = True
        self.start_menu_code = 0
        bool_mouse_pressed = False
        time_to_wait_before_press_again = 0

        #Code 0, les saves
        Bouton(self.screen, (0,-1/2), self.drawer.bouton_size, "Sauvegarde 1", "save 1")
        Bouton(self.screen, (0,0), self.drawer.bouton_size, "Sauvegarde 2", "save 2")
        Bouton(self.screen, (0,1/2), self.drawer.bouton_size, "Sauvegarde 3", "save 3")
        #Code 1, launch
        Bouton(self.screen, (0,1/3), self.drawer.bouton_size, "Jouer", "launch", 1)
        Bouton(self.screen, (0,-1/2), self.drawer.bouton_size, "Retour", "retour", 1)


        while self.running_start_menu:
            t1 = time.time()
            #Inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Bouton.erased(range(0,9+1))
                    self.running = False
                    self.running_start_menu = False

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RETURN]:
                self.start_menu_active = True
            if key_pressed[pygame.K_ESCAPE]:
                self.start_menu_active = False
                self.start_menu_code = 0
            
            #Actions des boutons
            if Bouton.last_return == "save 1":
                Bouton.last_return = ""
                self.start_menu_code = 1
                Save.choice_save(1)
                if len(Save.save)==0:texte_save_to_print = "SAUVEGARDE VIDE"
                else: texte_save_to_print = f"Vous êtes à {Save.save["player"]["zone"]}"
                self.drawer.draw_text_on_screen(texte_save_to_print, (255,255,255),(self.screen.get_width()/2,self.screen.get_height()/2),txt_size=20)
            elif Bouton.last_return == "save 2":
                Bouton.last_return = ""
                self.start_menu_code = 1
                Save.choice_save(2)
                if len(Save.save)==0:texte_save_to_print = "SAUVEGARDE VIDE"
                else: texte_save_to_print = f"Vous êtes à {Save.save["player"]["zone"]}"
                self.drawer.draw_text_on_screen(texte_save_to_print, (255,255,255),(self.screen.get_width()/2,20),txt_size=20,bold=True)
            elif Bouton.last_return == "save 3":
                Bouton.last_return = ""
                self.start_menu_code = 1
                Save.choice_save(3)
                if len(Save.save)==0:texte_save_to_print = "SAUVEGARDE VIDE"
                else: texte_save_to_print = f"Vous êtes à {Save.save["player"]["zone"]}"
                self.drawer.draw_text_on_screen(texte_save_to_print, (255,255,255),(self.screen.get_width()/2,20),txt_size=20,bold=True)
            elif Bouton.last_return == "retour":
                Bouton.last_return = ""
                self.start_menu_code = 0
            elif Bouton.last_return == "launch":
                Bouton.erased(range(0,9+1))
                Bouton.last_return == ""
                self.running_start_menu = False
                

            #Draw le background et boutons
            self.drawer.draw_on_screen(self.drawer.mainfond, (0,0), self.screen.get_size())
            if self.start_menu_active:
                self.drawer.draw_dark_on_screen(127)
                bool_mouse_pressed = Bouton.active_all(self.start_menu_code, time_to_wait_before_press_again<0)
            else:
                self.drawer.draw_text_on_screen_not_rel("Appuyez sur ENTER pour jouer", (255,255,255),(10,self.screen.get_height()-40),txt_size=14,italic=True)

            t2 = time.time()
            self.fps = max(round(1/(max(t2-t1,0.0001))),self.SEUIL_FPS)
            
            #Limiter le click de la sourie
            if bool_mouse_pressed:
                time_to_wait_before_press_again = 0.4
            time_to_wait_before_press_again -= (t2-t1)
                
            pygame.display.flip()




#FONCTIONS UTILITAIRES DANS LES AUTRES
#On initialise le groupe des objets de la carte
    def create_group(self):
        #Créer le groupe
        self.group = pyscroll.PyscrollGroup(self.map_manager.map_layer, default_layer=5)
        self.group.add(self.player)

#On récupère les données des collisions
    def get_objects_from_tmx_data(self):
        #Collisions et Exits, récupérer les groupes d'objets d'une classe spécifique
        self.group_collisions_retcs = []   ;self.group_collisions_retcs : list[pygame.Rect]
        self.group_exits = []              ;self.group_exits : list[dict]
        self.group_exits_rects = []        ;self.group_exits_rects : list[pygame.Rect]

        for obj_collision in self.map_manager.tmx_data.objects:
            if obj_collision.type == "collision":
                self.group_collisions_retcs.append(pygame.Rect(obj_collision.x,obj_collision.y,obj_collision.width,obj_collision.height))
            elif obj_collision.type == "exit":
                self.group_exits.append({"name":obj_collision.name, "rect":pygame.Rect(obj_collision.x,obj_collision.y,obj_collision.width,obj_collision.height)})
                self.group_exits_rects.append(pygame.Rect(obj_collision.x,obj_collision.y,obj_collision.width,obj_collision.height))

#Charger tous les ojets et leurs propriétés
    def reload_groups(self):
        self.create_group()
        self.player.tp_sprite_to((self.player.old_pos[0],self.player.old_pos[1]))
        self.get_objects_from_tmx_data()

    def load_groups_at_enter(self, which_enter:str):
        self.create_group()

        #Placer le joueur à sa position de départ
        object_for_player_pos = self.map_manager.tmx_data.get_object_by_name(which_enter)    #main_enter : nom du point de départ principal
        self.player.tp_sprite_to((object_for_player_pos.x,object_for_player_pos.y))

        self.get_objects_from_tmx_data()  
      
#Sauvegarder la partie
    def to_save(self)->None:
        save = {}
        save["player"] = self.player.to_save()

        Save.to_save(save)

#Récup les touches
    def handle_keyboard_inputs(self):
        input_pressed = pygame.key.get_pressed()

        #Quitter - - > Menu
        if input_pressed[pygame.K_ESCAPE]:
            self.running = False
        #Mettre toutes les variables à save dans save
        if input_pressed[pygame.K_p]:
            self.to_save()

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

#Vérifier les collisions et agir en fonction
    def verif_player_collisions(self)->None:
        #Vérifications exit, l'utilisation d'un test avant d'itérer tous les éléments pour chercher avec lequel le perso est en collision est plus optimisé
        if self.player.feet.collidelist(self.group_exits_rects) > -1:
            for exit_collision in self.group_exits:
                if self.player.feet.colliderect(exit_collision["rect"]):   #Rect de l'exit
                    self.map_manager.switch_map(self.player,exit_collision["name"])   #Name de l'exit
                    self.load_groups_at_enter(self.map_manager.cardinal_point_convert(self.player, exit_collision["name"]))

        #Vérifications colisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.group_collisions_retcs) > -1:
                sprite.move_back()




#GROUPES DE FONCTIONS DANS LA BOUCLE RUNNING
#Récup tous les éléments relatifs au jeu en général, style quitter, menu ...
    def catch_events(self)->None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE or event.type == pygame.VIDEOEXPOSE:
                self.reload_groups()

        self.handle_keyboard_inputs()
        self.handle_player_inputs()

#Bouger les sprites en fonctions de leurs colisions
    def move_sprites(self)->None:
        self.player.move(self.fps)

#Mettre à jour les objets sur la carte
    def update_objects(self)->None:
        self.group.update()
        self.verif_player_collisions()

#Afficher les updates
    def paint(self)->None:
        #Après que layer group ait été update
        self.group.draw(self.screen)
        
#Bouger la caméra avec le joueur
    def update_camera(self)->None:
        self.group.center(self.player.pos)

#Retourner des infos de fonctionnement du jeu
    def get_stats_info_running(self)->None:
        #self.true_fps = self.clock.get_fps()
        pass




#
#Fonction centrale du programme
    def run(self)->None:
        pygame.font.init()

        #True pour que le jeu tourne
        self.running = True
        self.running_start_menu = True

        #Main menu
        self.start_menu()

        if self.running:
            #Initialisation du jeu
            self.load_save()
            self.init_map_groups()

            #Clock pr les fps askip
            self.clock = pygame.time.Clock()


        #Boucle du jeu
        while self.running:
            #Start de boucle
            t1 = time.time()


            #Evènements dont touches
            self.catch_events()

            #Agir sur les objets
            self.move_sprites()
            self.update_objects()
            
            #Affichage
            self.paint()
            self.update_camera()
            pygame.display.flip()
            
            #Running correctly
            self.get_stats_info_running()


            #End de boucle
            t2 = time.time()
            #fps réajusté
            self.fps = max(round(1/(max(t2-t1,0.0001))),self.SEUIL_FPS)
            #On ralentit un peu
            time.sleep(0.001)

        #Relancer le game mais au main menu ou False
        return False