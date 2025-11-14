import pygame, pytmx, pyscroll
from src.player import Player
class Map_Manager():

    DICT_TRANSITIONS_ZONES = {}

    def __init__(self, screen):
        #Inits du Game()
        self.screen = screen

        #Inits des listes de données à prendre en compte
        self.LISTE_TRANSITIONS_ZONES = Map_Manager.DICT_TRANSITIONS_ZONES.keys()

        #Load les données -> à exporter
        self.tmx_data = pytmx.util_pygame.load_pygame("img/assets/cartes/rouilny/map_rouilny_0_0.tmx")
        
        #Récupérer les données pour pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        #Les calques
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2


    def cardinal_point_convert(self, exit_name:str|None="main_exit")->str:
        if exit_name == "ouest_exit":
            return "est_enter"
        elif exit_name == "est_exit":
            return "ouest_enter"
        elif exit_name == "nord_exit":
            return "sud_enter"
        elif exit_name == "sud_exit":
            return "nord_enter"
        elif exit_name == "main_exit":
            return "main_enter"
        elif exit_name in self.LISTE_TRANSITIONS_ZONES:
            return Map_Manager.DICT_TRANSITIONS_ZONES[exit_name]
        else:
            assert NameError(name=exit_name)


    def switch_map(self, player:Player, exit_name:str|None="main_exit")->None:
        #On imagine qu'il n'y pas de zone exit ni de exit différent d'un cardinal
        to_this_zone = player.zone
        if exit_name in ["ouest_exit","est_exit","nord_exit","sud_exit"]:
            if exit_name == "ouest_exit":
                to_this_troncon = (player.troncon[0]-1,player.troncon[1])
            elif exit_name == "est_exit":
                to_this_troncon = (player.troncon[0]+1,player.troncon[1])
            elif exit_name == "nord_exit":
                to_this_troncon = (player.troncon[0]-1,player.troncon[1])
            elif exit_name == "sud_exit":
                to_this_troncon = (player.troncon[0]+1,player.troncon[1])
        else:
            pass   #Tester les zones (mais avant), les sortes de sous-zones (batiments ou main)
        
        #Important de modif la position de player
        player.zone = to_this_zone
        player.troncon = to_this_troncon

        #Load les données -> à exporter
        self.tmx_data = pytmx.util_pygame.load_pygame(f"img/assets/cartes/{to_this_zone}/map_{to_this_zone}_{to_this_troncon[0]}_{to_this_troncon[1]}.tmx")
        
        #Récupérer les données pour pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        #Les calques
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2
