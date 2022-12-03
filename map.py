import pygame
import pytmx
import pyscroll

class Map:

    def __init__(self, chemin, layer, fenetre, zoom):

        self.layer = layer
        self.chemin = chemin
        self.fenetre = fenetre
        self.zoom = zoom

        #Permet de charger la carte
        self.maptmx = pytmx.util_pygame.load_pygame(f"Map/{self.chemin}")   #On va chercher le fichier
        self.mapdata = pyscroll.data.TiledMapData(self.maptmx)
        self.maplayer = pyscroll.orthographic.BufferedRenderer(self.mapdata, self.fenetre.get_size())
        self.maplayer.zoom = self.zoom   #On defini un zoom

        # Dessine les calques permettant d'afficher la carte
        self.calques = pyscroll.PyscrollGroup(map_layer = self.maplayer, default_layer = self.layer)


    def get_map_name(self):
        return self.chemin

    def get_map(self):
        return self.maptmx

    def get_calques(self):
        return self.calques

    def ajouter_joueur(self, joueur):
        self.calques.add(joueur)


    def charger_collisions(self):
        #On importe les zones de collision
        self.collisions = []
        for objet in self.maptmx.objects:
            if objet.name == "collision":
                self.collisions.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))

        return self.collisions

    def charger_hautes_herbes(self):
        #On importe les zones de collision
        self.hautes_herbes = []
        for objet in self.maptmx.objects:
            if objet.name == "hautes_herbes":
                self.hautes_herbes.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))

        return self.hautes_herbes
