import pygame
import pytmx

class Teleportation():

    def __init__(self):
        self.dico_teleportations = {
            "start" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "départ_joueur"}
            },
            "map.tmx" : {
                "maison_1" : {"monde_arr": "map_losange.tmx", "pos_arr": "depuis_map"},
                "maison_2" : {"monde_arr": "map_losange.tmx", "pos_arr": "depuis_map"},
                "maison_3" : {"monde_arr": "map_losange.tmx", "pos_arr": "depuis_map"}
            },
            "map_losange.tmx" : {
                "map" : {"monde_arr": "map.tmx", "pos_arr": "depuis_losange"}
            }
                }

    def get_dico_tp(self):
        return self.dico_teleportations
