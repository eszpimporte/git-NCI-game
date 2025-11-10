import pygame, pytmx, pyscroll

class Map_Manager():
    def __init__(self, screen):
        #Inits du Game()
        self.screen = screen


        #Load les données -> à exporter
        self.tmx_data = pytmx.util_pygame.load_pygame("img/assets/cartes/map_rouilny_0_0.tmx")
        
        #Récupérer les données pour pyscroll
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        
        #Les calques
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 1.5


    def switch_map(self):
        pass