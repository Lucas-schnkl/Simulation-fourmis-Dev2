import random
from fourmis import Soldat
import environnement

class Predateur:
    liste_predateurs = []
    def __init__(self,envi , pos_x:int = 0, pos_y:int = 0, couleur="#FF0000", fuite:bool = False ):
        self._envi = envi
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._couleur = couleur
        self._fuite = fuite

        self.delais = 0
        self.pos_a_fuir = []
        self.liste_predateurs.append(self)

    def __repr__(self):
        return f"Predateur(x={self.pos_x}, y={self.pos_y} , fuite={self._fuite})"
    
    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x):
        self._pos_x = x

    #position y
    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self,y):
        self._pos_y = y

    @property
    def fuite(self):
        return self._fuite
    
    @fuite.setter
    def fuite(self, valeur):
        self._fuite = valeur
        #print("predateur en fuite")

    def manger(self,env):
        for fourmis in env.fourmis:
            diff_x = abs(self.pos_x - fourmis.pos_x)
            diff_y = abs(self.pos_y - fourmis.pos_y)
            if (diff_x <= 1 and diff_y <= 1):
                fourmis.vivante = False
    
    def confrontation(self):
        self.pos_a_fuir = []
        for soldat in Soldat.liste_soldats:
            diff_x = abs(self.pos_x - soldat.pos_x)
            diff_y = abs(self.pos_y - soldat.pos_y)
            
            if (diff_x <= 1 and diff_y <= 1):
                self.fuite = True
                self.delais = 0
                self.pos_a_fuir = [soldat.pos_x, soldat.pos_y, self.pos_x, self.pos_y]

                #Soldat active phéro de danger
                soldat.deposer_pheromones_danger(self._envi)
                break

        if self.fuite:
            self.delais += 1
            if self.delais >= 5:
                self.fuite = False
                self.delais = 0

    def se_deplacer(self, env):
        self.confrontation()
        if not self.fuite:
            # Choisit direction au hasard
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # met nouvelles coordonnées dans variables temporaires
            nx = self.pos_x + dx
            ny = self.pos_y + dy

            # applique changements de position
            if 0 <= nx < self._envi.largeur_grille and 0 <= ny < self._envi.hauteur_grille:
                self.pos_x = nx
                self.pos_y = ny

            # Vérif limites grille
            if 0 <= nx < self._envi.largeur_grille and 0 <= ny < self._envi.hauteur_grille:
                self.pos_x = nx
                self.pos_y = ny

        elif len(self.pos_a_fuir) == 4:
            soldat_x, soldat_y, moi_x, moi_y = self.pos_a_fuir
            dx = moi_x - soldat_x
            dy = moi_y - soldat_y                #inshallah ca fonctionne / Hg yourself ca marche pas je l'ai changé bisou bisou

            #evite les bug de saut de case
            if dx > 1: dx = 1
            if dx < -1: dx = -1
            if dy > 1: dy = 1
            if dy < -1: dy = -1

            # met nouvelles coordonnées dans variables temporaires
            nx = self.pos_x + dx
            ny = self.pos_y + dy

            # Vérification limites grille
            if 0 <= nx < self._envi.largeur_grille and 0 <= ny < self._envi.hauteur_grille:
                self.pos_x = nx
                self.pos_y = ny