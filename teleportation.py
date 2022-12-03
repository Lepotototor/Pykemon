import pygame
import pytmx

class Teleportation():

    """
    Classe qui sert comme une base de donnée pour la gestion de changement de map
    """

    def __init__(self):
        self.dico_teleportations = {
            "start" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "départ_joueur"}
            },
            "map.tmx" : {
                "Maison_joueur" : {"monde_arr": "Maison_joueur.tmx", "pos_arr": "départ_joueur"},
                "Maison_professeur" : {"monde_arr": "Maison_professeur.tmx", "pos_arr": "départ_joueur"},
                "map_losange" : {"monde_arr": "map_losange.tmx", "pos_arr": "depuis_map"}
            },
            "Maison_joueur.tmx" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "départ_joueur"}
            },
            "Maison_professeur.tmx" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "départ_professeur"}
            },
            "map_losange.tmx" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "depuis_losange"}
            }
                }

        self.infos_maps = {
            "map.tmx" : {"layer" : 8, "zoom": 5},
            "map_losange.tmx" : {"layer" : 8, "zoom": 5},
            "Maison_joueur.tmx" : {"layer" : 4, "zoom": 4},
            "Maison_professeur.tmx" : {"layer" : 4, "zoom": 4},
        }

    def get_dicos(self):
        """Sert à récupérer la 'base de données' """
        return self.dico_teleportations, self.infos_maps
