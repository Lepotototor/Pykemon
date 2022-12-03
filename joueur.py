import pygame

#On créé une classe en mettant en allant chercher la fonction de pygame pour recuperer les sprites
class Joueur(pygame.sprite.Sprite):

    def __init__(self, position):
        #constructeur prenant en argument la position du joueur
        super().__init__()   #Je sais pas a quoi ca sert mais pygame en a besoin pour charger le sprite
        self.sprite_sheet = pygame.image.load("./Sprites/MainPlayer.png")   #On indique le chemin de l'image a charger
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (48, 68))   #On redimensionne l'image
        self.image = self.get_image((0, 0))
        self.image.set_colorkey((0, 0, 0))    #On enleve le fond noir de l'image
        self.rect = self.image.get_rect()    #On recupere la zone on sera mis l'image
        self.position = position     #position ou charger le joueur
        self.bas_du_joueur = pygame.Rect(0, 0, self.rect.width/2, 5)      #Variable qui sert de point de repere pour les collisions,
                                                #donne l'impression de 3D et evite de bloquer si c'est la tete du joueur qui est en contact avec un obstacle
        self.ancienne_position = self.position_avant()       #On sauvegarde la position
        self.directions = self.charger_directions()        #On charge le dictionnaire des directions
        self.ancienne_direction = None
        self.compteur = 0
        self.frame = 0          #Permet d'avoir une animation plus épurée et évite l'impression de semi-marathon


    def get_position(self):
        return self.position

    def get_ancienne_position(self):
        return self.ancienne_position

    def set_position(self, nv_position):
        self.position = nv_position.copy()


    def droite(self):
        self.position[0] += self.vitesse
        self.animation("droite")

    def gauche(self):
        self.position[0] -= self.vitesse
        self.animation("gauche")

    def haut(self):
        self.position[1] -= self.vitesse
        self.animation("haut")

    def bas(self):
        self.position[1] += self.vitesse
        self.animation("bas")



    def animation(self, direction):
        self.frame += 1
        #Permet justement de changer l'animation moins souvent
        if self.frame == 40:
            if direction == self.ancienne_direction:
                #Si le joueur continue dans la même direction on fait avancer l'animation
                self.compteur += 1
                #Permet de naviguer entre les différentes positions
                if (self.compteur > 3):
                    self.compteur = 0
            else:
                self.compteur = 0
            self.frame = 0
        #On applique le changement d'image
        self.image = self.get_image(self.directions[direction][self.compteur])
        self.ancienne_direction = direction

    def charger_directions(self):
        """
        Permet juste de créer un dictionnaire avec la position de chaque rectangle de
        chaque position du Joueur
        """
        dico_positions = {}
        dico_positions["bas"] = [(x,0) for x in range(4)]
        dico_positions["gauche"] = [(x,1) for x in range(4)]
        dico_positions["droite"] = [(x,2) for x in range(4)]
        dico_positions["haut"] = [(x,3) for x in range(4)]
        return dico_positions


    def position_avant(self):
        """Enregistre la position actuelle du joueur"""
        self.ancienne_position = self.position.copy()


    def update(self):
        """ Methode permettant de mettre a jour la position du joueur
        """
        self.rect.topleft = self.position   #permet d'actualiser la zone ou se charge l'image avec la position du joueur
        self.bas_du_joueur.midbottom = self.rect.midbottom


    def retour_arrriere(self):
        """Remet le joueur à son ancienne position """
        self.position = self.ancienne_position
        self.update()


    def get_image(self, position):
        """ Fonction qui permet de definir la surface ou mettre le sprites
            a partir de coordonnees et vient y mettre l'image
        """
        image = pygame.Surface([12, 17])   #On défini la surface que va occuper l'image
        image.blit(self.sprite_sheet, (0, 0), (position[0]*12, position[1]*17, 12, 17))   #On defini où on met l'image par rapport a la surface(au meme endroit que la surface)
                                                                  #Et on defini quelle partie de l'image on place ou
        return image
