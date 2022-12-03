import pygame
import pytmx
import pyscroll
import sys
import random
import csv

from joueur import Joueur
from map import Map
from teleportation import Teleportation


def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/font.ttf", size)


class Jeux:

    def __init__(self):
        #constructeur

        self.fenetre = pygame.display.set_mode((1280, 720))   #On defini la fenetre
        pygame.display.set_caption("Pykemon")   #Avec son titre

        # Variable de boucle
        self.jeu_encours = True

        #On importe tous les points de téléportation
        self.teleportations, self.infos_maps = Teleportation().get_dicos()

        self.changement_map(self.teleportations["start"]["map"])

        self.sauvergarde_position = self.joueur.get_position().copy()





    def entrees_clavier(self):
        """
            Fonction qui sers a faire avancer le joueur .

            Dans un premier temps la touche CTRL est vérifié , si celle-ci est pressé
            la vitesse du joueur sera augmentée , si elle ne l'est pas la vitesse
            sera celle de base .


            Puis on verifie  :
                    si la touche UP est pressé on modifie la position du joueur et
                    on la déplace vers le haut

                    si la touche DOWN est pressé on modifie la position du joueur et
                    on la déplace vers le bas

                    si la touche RIGHT est pressé on modifie la position du joueur et
                    on la déplace vers la droite

                    si la touche LEFT est pressé on modifie la position du joueur et
                    on la déplace vers la gauche
        """
        pressé=pygame.key.get_pressed()

        if pressé[pygame.K_LCTRL] :
            self.joueur.vitesse=0.5
        else:
            self.joueur.vitesse=0.25

        if pressé[pygame.K_UP]:
            self.joueur.haut()
        elif pressé[pygame.K_DOWN]:
            self.joueur.bas()
        elif pressé[pygame.K_LEFT]:
            self.joueur.gauche()
        elif pressé[pygame.K_RIGHT]:
            self.joueur.droite()

        elif (pressé[pygame.K_RETURN]) and (self.joueur.get_position() != self.sauvergarde_position):
            self.sauvergarde()
            print("sauvergardé")
        elif (pressé[pygame.K_r]) and (self.joueur.get_position() != self.sauvergarde_position):
            self.restaure()
            print("restauré")


        self.joueur.image.set_colorkey((0, 0, 0))    #On enleve le fond noir de l'image

    def sauvergarde(self):
        self.sauvergarde_position = self.joueur.get_position().copy()
        with open('.sauvergarde.csv','w',newline='') as fichiercsv:
            writer=csv.writer(fichiercsv)
            writer.writerow([self.map.get_map_name(), self.sauvergarde_position[0], self.sauvergarde_position[1]])

    def restaure(self):
        file = open(r".sauvergarde.csv")
        reader_file = csv.reader(file)
        for row in reader_file:
            nv_map = row[0]
            nv_position = [ float(row[1]), float(row[2]) ]
            print(type(nv_position))
            print(nv_map, nv_position)

        #On charge la map et ses données relatives
        self.map = Map(nv_map, self.infos_maps[nv_map]["layer"], self.fenetre, self.infos_maps[nv_map]["zoom"])
        self.collisions = self.map.charger_collisions()
        self.hautes_herbes = self.map.charger_hautes_herbes()

        #On charge les données du joueur
        self.joueur = Joueur(nv_position)
        self.map.ajouter_joueur(self.joueur)



    def detecte_collision(self):
        """
        fontion ou l'on detecte les collisions, on met aussi a jour l'affichage
        si le joueur est sur une zone de collision on le remet a une position ou
        il n'etait pas sur une collision
        """

        sprite = self.map.get_calques().sprites()[0]
        #On verifie si la zonedu bas du joueur entre en collision avec un rectangle de collision
        if sprite.bas_du_joueur.collidelist(self.collisions) != -1:
            sprite.retour_arrriere()

    def detecte_combat(self):
        """
        fontion ou l'on detecte les collisions, on met aussi a jour l'affichage
        si le joueur est sur une zone de collision on le remet a une position ou
        il n'etait pas sur une collision
        """

        sprite = self.map.get_calques().sprites()[0]
        #print(self.hautes_herbes)
        #On verifie si la zonedu bas du joueur entre en collision avec un rectangle de collision
        if (self.joueur.get_position() != self.joueur.get_ancienne_position()) and (sprite.bas_du_joueur.collidelist(self.hautes_herbes) != -1):
            #print("possible")
            if (random.randint(0, 300) == 0):
                print("COMBAT !!")



    def detecte_teleportation(self):
        """
        Permet de détecter si le joueur entre en collision avec une zone de téléportation
        """
        map_name = self.map.get_map_name()

        sprite = self.map.get_calques().sprites()[0]
        tp_map = self.teleportations[map_name]

        for point_tp in tp_map.keys():
            objet = self.map.get_map().get_object_by_name(point_tp)
            teleport = [pygame.Rect(objet.x, objet.y, objet.width, objet.height)]
            #Pour chaque zone de teleportation de la map
            #On verifie si le joueur y est en contact

            if sprite.bas_du_joueur.collidelist(teleport) != -1:
                self.changement_map(self.teleportations[map_name][point_tp])
                #On change de map en allant interroger la 'bas de données'
                break


    def changement_map(self, point_tp):
        #On charge les données utiles au nouvel emplacement du joueur
        nv_monde = point_tp["monde_arr"]
        pos_joueur = point_tp["pos_arr"]

        #On charge la map et ses données relatives
        self.map = Map(nv_monde, self.infos_maps[nv_monde]["layer"], self.fenetre, self.infos_maps[nv_monde]["zoom"])
        self.collisions = self.map.charger_collisions()
        self.hautes_herbes = self.map.charger_hautes_herbes()

        #On charge les données du joueur
        position_joueur = self.map.maptmx.get_object_by_name(pos_joueur)
        self.joueur = Joueur([position_joueur.x, position_joueur.y])
        self.map.ajouter_joueur(self.joueur)


    def run(self):

        # Mise en place de la 'clock' qui va s'occuper d'es frames par seconde
        clock = pygame.time.Clock()
        FPS = 250

        #creation de la boucle de jeu
        while self.jeu_encours:

            clock.tick(FPS)
            #FPS = clock.get_fps()

            #On enregistre la position du joueur au cas ou il irait sur une zone de collision
            self.joueur.position_avant()

            # On verifie si il y a une entrée de la part du joueur
            self.entrees_clavier()

            #On met a jour les calques de la map
            self.map.get_calques().update()

            #On remmet le joueur la ou il etait si il est sur une zone de collisions
            self.detecte_teleportation()
            self.detecte_collision()
            self.detecte_combat()

            #On actualise la position du joueur
            self.map.calques.center(self.joueur.rect)   #On centre la fenetre de jeu autour du joueur

            # Dessine la carte
            self.map.calques.draw(self.fenetre)
            pygame.display.flip()   # Permet de rafraichir

            for event in pygame.event.get():
                #evenement pour fermer la fenetre
                if event.type == pygame.QUIT:
                    self.jeu_encours = False


        pygame.quit()
