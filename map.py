import pygame
import pytmx
import pyscroll

class Map:

    def __init__(self, chemin, layer, fenetre, zoom=3):

        self.layer = layer
        self.chemin = chemin
        self.fenetre = fenetre
        self.zoom = zoom

        #Permet de charger la carte
        self.maptmx = pytmx.util_pygame.load_pygame(self.chemin)   #On va chercher le fichier
        self.mapdata = pyscroll.data.TiledMapData(self.maptmx)
        self.maplayer = pyscroll.orthographic.BufferedRenderer(self.mapdata, self.fenetre.get_size())
        self.maplayer.zoom = self.zoom   #On defini un zoom

        # Dessine les calques permettant d'afficher la carte
        self.calques = pyscroll.PyscrollGroup(map_layer = self.maplayer, default_layer = self.layer)


    def charger_collisions(self):
        #On importe les zones de collision
        self.collisions = []
        #print(maptmx.objects)
        for objet in self.maptmx.objects:
            if objet.name == "collision":
                self.collisions.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        #print(self.collisions)

    def charger_teleportation(self):
        self.teleportations = []
        print(self.maptmx.get_object_by_class("collision"))
        for objet in self.maptmx.objects:
            #print(objet)
            if objet.name == 'téléportation':
                print(objet)
