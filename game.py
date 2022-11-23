import pygame , sys 
import pytmx
import pyscroll
from button import Button

from joueur import Joueur
from map import Map

def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/font.ttf", size)


class Jeux:

    def __init__(self):
        #constructeur
        self.fenetre = pygame.display.set_mode((800, 600))   #On defini la fenetre
        pygame.display.set_caption("Pykemon")   #Avec son titre

        # Variable de boucle
        self.jeu_encours = True


        #On charge la map
        self.map = Map("map.tmx", 12, self.fenetre)
        self.map.charger_collisions()

        #On charge les données du joueur
        position_joueur = self.map.maptmx.get_object_by_name("départ_joueur")
        self.joueur = Joueur([position_joueur.x, position_joueur.y])
        self.map.calques.add(self.joueur)




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
        elif pressé[pygame.K_a]:
            #On charge la map
            self.map = Map("map_losange.tmx", 12, self.fenetre)
            self.map.charger_collisions()

            #On charge les données du joueur
            position_joueur = self.map.maptmx.get_object_by_name("départ_joueur")
            self.joueur = Joueur([position_joueur.x, position_joueur.y])
            self.map.calques.add(self.joueur)


        self.joueur.image.set_colorkey((0, 0, 0))    #On enleve le fond noir de l'image


    def detecte_collision(self):
        """
        fontion ou l'on detecte les collisions, on met aussi a jour l'affichage
        si le joueur est sur une zone de collision on le remet a une position ou
        il n'etait pas sur une collision
        """
        self.map.calques.update()

        for sprite in self.map.calques.sprites():
            if sprite.bas_du_joueur.collidelist(self.map.collisions) > -1:
                sprite.retour_arrriere()
                
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

            #On remmet le joueur la ou il etait si il est sur une zone de collisions
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
