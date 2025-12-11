import random

class Predateur:
    liste_predateurs = []
    def __init__(self,envi , pos_x:int = 0, pos_y:int = 0, couleur="#FF0000", fuite:bool = False ):
        self._envi = envi
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._couleur = couleur
        self._fuite = fuite

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
        global delais
        delais = 0
        self._fuite = valeur
        print("predateur en fuite")
    
    def confrontation(self):
        global pos_a_fuir
        pos_a_fuir = []
        for soldat in liste_soldats:
            diff_x = abs(self.pos_x - soldat.pos_x)
            diff_y = abs(self.pos_y - soldat.pos_y)
            
            if (diff_x <= 1 and diff_y <= 1) and not (diff_x == 0 and diff_y == 0):
                self.fuite = True
                pos_a_fuir.append(soldat.pos_x,soldat.pos_y , self.pos_x , self.pos_y)
                break
            if delais:
                delais = delais + 1
                if delais == 5:
                    self.fuite = False

    def se_deplacer(self):
        self.confrontation()
        if self.fuite == False:
            # Choisit direction au hasard
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # met nouvelles coordonnées dans variables temporaires
            nx = self.pos_x + dx
            ny = self.pos_y + dy

            # applique changements de position
            self.pos_x = nx
            self.pos_y = ny

        else:
            dx = pos_a_fuir[2] - pos_a_fuir[0]
            dy = pos_a_fuir[3] - pos_a_fuir[1]                 #inshallah ca fonctionne

            # met nouvelles coordonnées dans variables temporaires
            nx = self.pos_x + dx
            ny = self.pos_y + dy

            # applique changements de position
            self.pos_x = nx
            self.pos_y = ny