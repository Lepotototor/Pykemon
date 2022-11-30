import pygame
import pytmx
import pyscroll
import sys

from game import Jeux
from joueur import Joueur
from map import Map
from teleportation import Teleportation

def get_font(size):
            """
                -Cette fonction est une fonction permettant d'importer le 'font' , la police d'écriture
                qui sera visible sur le menu et les buttons

                - la on import l'image 'font.ttf' est importé 
            
            """
            return pygame.font.Font("assets/font.ttf", size)



class Menu :
    def __init__(self) :
        """
          -Le constructeur ne prend en argument aucune valeur ,vartiable,ect...
          -Elle a seulement besoin du self 
        """
        pass

    
    def main_menu(self):
        """
          - La fonction main_menu , est une fonction permettant d'afficher le menu de demarage
            qui est visble lors du lancement du jeux.
            
          -Cette fonction , dans un premier temps creer la fenetre , c'est la variable SCREEN
          
          -Puis elle import , la zone qui servira a la detection des différents buttons
            et également l'image qui servira de fond a l'écran de menu
            
          - Et donc pour finir elle boucle pour pouvoir :
              -rafraichir la position de la souris qui est verifié a chaque instant
              -créer et afficher les buttons et le titre "PYKEMON" , avec differents position , couleur
                et interaction possible (hovering)
              -lancer le fichier run() si le button JOUER est pressé
              -fermer la fenetre si le button QUITTER et cliqué 
            
        """
        pygame.init()
        SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")
        image=pygame.image.load("assets/Options Rect.png")


        BG = pygame.image.load("assets/fond.jpg")


        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("PYKEMON ", True, (182,143,64, 0.8))
            MENU_RECT = MENU_TEXT.get_rect(center=(700, 100))

            PLAY_BUTTON = Button(image, pos=(640, 230),
                                    text_input="JOUER",  font=get_font(60),base_color=(255,255,255), hovering_color=(0,0,0))

            QUIT_BUTTON = Button(image, pos=(640, 425),
                                    text_input="QUITTER", font=get_font(40), base_color=(255,0,0), hovering_color=(0,0,0))

            SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON,QUIT_BUTTON]:
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
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()





class Button():
    
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
                """
                        -le constructeur initialise tout les variable nécéssair aux
                            -couleur des buttons
                            -position x et y de la souris
                            -les images des buttons (là , il récupere leur longeur est hauteur qui
                             servirons plus tard a savoir si la postion est sur le button)
                        

                """
                    
                self.image = image
                self.x_pos = pos[0]
                self.y_pos = pos[1]
                self.font = font
                self.base_color, self.hovering_color = base_color, hovering_color
                self.text_input = text_input
                self.text = self.font.render(self.text_input, True, self.base_color)
                if self.image is None:
                        self.image = self.text
                self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
                self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
                """
                    -fonction qui permet de prendre en compte la surface des buttons  
                """
                if self.image is not None:
                        screen.blit(self.image, self.rect)
                screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
                """
                    - fonction qui verifie  la position du curseur
            
                """
                if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                        return True
                return False

	def changeColor(self, position):
                """
                    - fonction qui verifie  la position du curseur
                    - et si le curseur est au dessus d'un button le changement de clicker est apliqué
                """
                if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
                        self.text = self.font.render(self.text_input, True, self.hovering_color)
                else:
                        self.text = self.font.render(self.text_input, True, self.base_color)





