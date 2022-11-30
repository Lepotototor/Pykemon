import pygame

from menu import Menu
from game import Jeux

#Boucle qui sert à initialiser le jeux
if __name__ == "__main__":
    pygame.init()
    menu = Menu()
    menu.main_menu()
