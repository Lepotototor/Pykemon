import pygame
import pytmx
import pyscroll
import sys

from button import Button
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
        self.teleportations = Teleportation().get_dico_tp()

        self.changement_map(self.teleportations["start"]["map"])





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
            self.joueur.vitesse=0.2
        else:
            self.joueur.vitesse=0.15

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

        sprite = self.map.calques.sprites()[0]
        #print(sprite.bas_du_joueur.collidelist(self.collisions))
        if sprite.bas_du_joueur.collidelist(self.collisions) != -1:
            sprite.retour_arrriere()



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

            if sprite.bas_du_joueur.collidelist(teleport) != -1:
                self.changement_map(self.teleportations[map_name][point_tp])


    def changement_map(self, point_tp):
        #On charge les données utiles
        nv_monde = point_tp["monde_arr"]
        pos_joueur = point_tp["pos_arr"]

        #On charge la map et ses données relatives
        self.map = Map(nv_monde, 8, self.fenetre)
        self.collisions = self.map.charger_collisions()

        #On charge les données du joueur
        position_joueur = self.map.maptmx.get_object_by_name(pos_joueur)
        self.joueur = Joueur([position_joueur.x, position_joueur.y])
        self.map.ajouter_joueur(self.joueur)



    def main_menu():
        SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")

        BG = pygame.image.load("assets/Background.png")


        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                                text_input="PLAY",  font=get_font(75),base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75),base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        jeux = Jeux()
                        jeux.run()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

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
            self.map.calques.update()

            #On remmet le joueur la ou il etait si il est sur une zone de collisions
            self.detecte_teleportation()
            self.detecte_collision()

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
