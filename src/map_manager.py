import pygame, pytmx, pyscroll
from src.player import Player
from img.assets.cartes.ref_zones_changes import REF_SUBZONES, DICT_TRANSITIONS_ZONES

#Indications par rapport aux exits et enters :
#ATTENTION, CLASS ENTER et EXIT sur Tiled !!!! à la lettre près : "enter" et "exit"
#Les exits de points cardinaux "ouest", "est", "sud", "nord" restent dn la mm zone et bouge de tronçons de +1 ou -1 
#Les exits de sous-zones, batiments composés de qu'une entrée et sortie, s'écrivent avec "subexit_{X}" et l'enter avec "subenter_{X}" dans la zone princ, X étant le nom de la sous-zone unique à la zone
#Les subenter doivent être référencées dn le folder de la carte dans un programme python du nom ""
#L'entrée "main_enter" est dn les subzones (l'unique entrée), ou l'arrivée principale dn une zone de toutes parts
#La sortie de la sous-zone peut être tout et n'importe quoi
#Les exits de zones doivent être référencées avec des noms uniques dn tout le jeu et répertorié dans LISTE_TRANSITIONS_ZONES pr obtenir la zone ou aller et la position du troncon ou main

class Map_Manager():

    def __init__(self, screen, player:Player):
        #Inits du Game()
        self.screen = screen

        #Inits des listes de données à prendre en compte
        self.LISTE_TRANSITIONS_ZONES = DICT_TRANSITIONS_ZONES.keys()

        #Load les données -> à exporter
        if player.subzone != "None":
            self.tmx_data = pytmx.util_pygame.load_pygame(f"img/assets/cartes/{player.zone}/map_{player.zone}_{player.subzone}.tmx")
        else:
            self.tmx_data = pytmx.util_pygame.load_pygame(f"img/assets/cartes/{player.zone}/map_{player.zone}_{player.troncon[0]}_{player.troncon[1]}.tmx")
        
        #Récupérer les données pour pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        #Les calques
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2


    def cardinal_point_convert(self, player:Player, exit_name:str)->str:
        #Le joueur bouge selon les pts cardinaux
        if exit_name == "ouest_exit":
            return "est_enter"
        elif exit_name == "est_exit":
            return "ouest_enter"
        elif exit_name == "nord_exit":
            return "sud_enter"
        elif exit_name == "sud_exit":
            return "nord_enter"
        #Lorsque le joueur sort d une sous-zone
        elif player.subzone != "None":
            enter_to_return = f"subenter_{player.subzone}"
            return enter_to_return
        #Le joueur rentre dans une sous-zone
        elif exit_name[:7] == "subexit":
            return "main_enter"
        #Le joueur change de zone
        elif exit_name in self.LISTE_TRANSITIONS_ZONES:
            return DICT_TRANSITIONS_ZONES[exit_name]["enter_name"]
        else:
            assert NameError(name=exit_name)


    def switch_map(self, player:Player, exit_name:str)->None:
        bool_enter_subzone = False

        #Le joueur bouge selon les pts cardinaux
        if exit_name in ["ouest_exit","est_exit","nord_exit","sud_exit"]:
            to_this_zone = player.zone
            if exit_name == "ouest_exit":
                to_this_troncon = (player.troncon[0]-1,player.troncon[1])
            elif exit_name == "est_exit":
                to_this_troncon = (player.troncon[0]+1,player.troncon[1])
            elif exit_name == "nord_exit":
                to_this_troncon = (player.troncon[0]-1,player.troncon[1])
            elif exit_name == "sud_exit":
                to_this_troncon = (player.troncon[0]+1,player.troncon[1])
        
        #Le joueur sort d'une sous-zone
        elif player.subzone != "None":
            to_this_zone = player.zone
            to_this_troncon = (player.troncon[0],player.troncon[1])
        #Le joueur rentre dans une sous-zone
        elif exit_name[:7] == "subexit":
            to_this_zone = player.zone
            bool_enter_subzone = True
        #Le joueur change de zone
        else:
            pass   #Tester les changements de zone
        

        #Load les données -> à exporter
        if bool_enter_subzone:
            player.move_zone(player.zone, player.troncon, subzone=exit_name[8:])
            self.tmx_data = pytmx.util_pygame.load_pygame(f"img/assets/cartes/{to_this_zone}/map_{to_this_zone}_{player.subzone}.tmx")
        else:
            player.move_zone(to_this_zone, to_this_troncon)
            self.tmx_data = pytmx.util_pygame.load_pygame(f"img/assets/cartes/{to_this_zone}/map_{to_this_zone}_{to_this_troncon[0]}_{to_this_troncon[1]}.tmx")
        

        #Récupérer les données pour pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        #Les calques
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2
