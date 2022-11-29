import pygame
import pytmx
import pyscroll
import sys

from game import Jeux
from button import Button
from joueur import Joueur
from map import Map
from teleportation import Teleportation

def get_font(size): # Returns Press-Start-2P in the desired size
            return pygame.font.Font("assets/font.ttf", size)



class Menu :
    def __init__(self) :
        pass
    def main_menu(self):
        pygame.init()
        SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")
        image=pygame.image.load("assets/Options Rect.png")


        BG = pygame.image.load("assets/fond.jpg")


        while True:
            SCREEN.blit(BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(100).render("MAIN MENU", True, (182,143,64, 0.8))
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

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
