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
                "Maison_professeur" : {"monde_arr": "Maison_professeur.tmx", "pos_arr": "départ_joueur"}
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

    def get_dico_tp(self):
        """Sert à récupérer la 'base de données' """
        return self.dico_teleportations
