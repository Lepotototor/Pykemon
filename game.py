import pygame
import pytmx
import pyscroll

from joueur import Joueur



class Jeux:

    def __init__(self):
        #constructeur
        self.fenetre = pygame.display.set_mode((800, 600))   #On defini la fenetre
        pygame.display.set_caption("Pykemon")   #Avec son titre

        # Variable de boucle
        self.jeu_encours = True

        #Permet de charger la carte
        maptmx = pytmx.util_pygame.load_pygame("map.tmx")   #On va chercher le fichier
        mapdata = pyscroll.data.TiledMapData(maptmx)
        maplayer = pyscroll.orthographic.BufferedRenderer(mapdata, self.fenetre.get_size())
        maplayer.zoom = 3   #On defini un zoom

        # Dessine les calques permettant d'afficher la carte
        self.calques = pyscroll.PyscrollGroup(map_layer = maplayer, default_layer=12)

        #On charge les données du joueur
        position_joueur = maptmx.get_object_by_name("départ_joueur")
        self.joueur = Joueur([position_joueur.x, position_joueur.y])
        self.calques.add(self.joueur)

        #On importe les zones de collision
        self.collisions = []
        #print(maptmx.objects)
        for objet in maptmx.objects:
            if objet.name == "collision":
                self.collisions.append(pygame.Rect(objet.x, objet.y, objet.width, objet.height))
        #print(self.collisions)


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
            self.joueur.vitesse=0.3
        else:
            self.joueur.vitesse=0.2

        if pressé[pygame.K_UP]:
            self.joueur.haut()
        elif pressé[pygame.K_DOWN]:
            self.joueur.bas()
        elif pressé[pygame.K_LEFT]:
            self.joueur.gauche()
        elif pressé[pygame.K_RIGHT]:
            self.joueur.droite()


        self.joueur.image.set_colorkey((0, 0, 0))    #On enleve le fond noir de l'image


    def detecte_collision(self):
        """
        fontion ou l'on detecte les collisions, on met aussi a jour l'affichage
        si le joueur est sur une zone de collision on le remet a une position ou
        il n'etait pas sur une collision
        """
        self.calques.update()

        for sprite in self.calques.sprites():
            if sprite.bas_du_joueur.collidelist(self.collisions) > -1:
                sprite.retour_arrriere()


    def run(self):
        clock = pygame.time.Clock()  #permet de gerer les fps

        #creation de la boucle de jeu
        while self.jeu_encours:

            #On enregistre la position du joueur au cas ou il irait sur une zone de collision
            self.joueur.position_avant()

            # On verifie si il y a une entrée de la part du joueur
            self.entrees_clavier()

            #On remmet le joueur la ou il etait si il est sur une zone de collisions
            self.detecte_collision()

            #On actualise la position du joueur
            self.calques.center(self.joueur.rect)   #On centre la fenetre de jeu autour du joueur

            # Dessine la carte
            self.calques.draw(self.fenetre)
            pygame.display.flip()   # Permet de rafraichir

            for event in pygame.event.get():
                #evenement pour fermer la fenetre
                if event.type == pygame.QUIT:
                    self.jeu_encours = False

        clock.tick(120)

        pygame.quit()
