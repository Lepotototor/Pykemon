import pygame

#On créé une classe en mettant en allant chercher la fonction de pygame pour recuperer les sprites
class Joueur(pygame.sprite.Sprite):

    def __init__(self, position):
        #constructeur prenant en argument la position du joueur
        super().__init__()   #Je sais pas a quoi ca sert mais pygame en a besoin pour charger le sprite
        self.sprite_sheet = pygame.image.load("./Sprites/MainPlayer.png")   #On indique le chemin de l'image a charger
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (48, 68))   #On redimensionne l'image
        self.image = self.get_image(0, 0)
        self.image.set_colorkey((0, 0, 0))    #On enleve le fond noir de l'image
        self.rect = self.image.get_rect()    #On recupere la zone on sera mis l'image
        self.position = position     #position ou charger le joueur
        self.direction = {  "bas" : self.get_image(0, 0),
                            "gauche" : self.get_image(0, 17),
                            "droite" : self.get_image(0, 34),
                            "haut" : self.get_image(0, 51) }
        self.bas_du_joueur = pygame.Rect(0, 0, self.rect.width/2, 5)      #Variable qui sert de point de repere pour les collisions,
                                                #donne l'impression de 3D et evite de bloquer si c'est la tete du joueur qui est en contact avec un obstacle
        self.ancienne_position = self.position.copy()

    def droite(self):
        self.position[0] += self.vitesse
        self.change_direction("droite")

    def gauche(self):
        self.position[0] -= self.vitesse
        self.change_direction("gauche")

    def haut(self):
        self.position[1] -= self.vitesse
        self.change_direction("haut")

    def bas(self):
        self.position[1] += self.vitesse
        self.change_direction("bas")







    def change_direction(self, direction):
        self.image = self.direction[direction]


    def position_avant(self):
        self.ancienne_position = self.position.copy()


    def update(self):
        """ Methode permettant de mettre a jour la position du joueur
        """
        self.rect.topleft = self.position   #permet d'actualiser la zone ou se charge l'image avec la position du joueur
        self.bas_du_joueur.midbottom = self.rect.midbottom


    def retour_arrriere(self):
        self.position = self.ancienne_position
        self.update()


    def get_image(self, x, y):
        """ Fonction qui permet de definir la surface ou mettre le sprites
            a partir de coordonnees et vient y mettre l'image
        """
        image = pygame.Surface([12, 17])   #On défini la surface que va occuper l'image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 12, 17))   #On defini où on met l'image par rapport a la surface(au meme endroit que la surface)
                                                                  #Et on defini quelle partie de l'image on place ou
        return image
