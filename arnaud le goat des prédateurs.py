
class Predateur:
    def __init__(self,canvas, pos_x:int = 0, pos_y:int = 0, faim=True, couleur="#FF0000",vie=200,attaque=10, nb_a_manger = 1, statut:bool = True, cible = "", taille = 15):
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._faim = faim      # après combat faire dans une fct a part que sa faim True // faim = false le fera partir de la map
        self._couleur = couleur
        self._vie = vie
        self._attaque = attaque
        self._nb_a_manger = nb_a_manger  #nb de fourmis qu'il doit manger pour que faim passe à false
        self._statut = statut
        self._cible = cible
        self._taille = taille

    @property
    def taille(self):
        return self._taille
    @taille.setter
    def taille(self, taille):
        self._taille = taille

    @property
    def cible(self):
        return self._cible

    @cible.setter
    def cible(self, cible):
        self._cible = cible

    @property
    def vie(self):
        return self._vie

    @vie.setter
    def vie(self,vie):
        self._vie = vie
        if self._vie <= 0 :
            self._vie = 0
            self._statut = False

    @property
    def nb_a_manger(self):
        return self._nb_a_manger

    @nb_a_manger.setter
    def nb_a_manger(self,nb_a_manger):
        self._nb_a_manger = nb_a_manger
        if self._nb_a_manger <= 0 :
            self._faim = False

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



    def chasse(self):         #le but de cette fonction est de trouver la cible rechercher (ex fourmis pour oiseau), de se deplacer vers ses coos (avec des if), arriver a ses coos et se battre avec
        coos_cible = self.canvas.coords(self.cible)
        coos_simplifier = [
            coos_cible[0] + coos_cible[2],
            coos_cible[1] + coos_cible[3]
        ]

        if coos_cible[0] <= self.pos_x <= coos_cible[2] and coos_cible[1] <= self.pos_y <= coos_cible[3] or coos_cible[2] <= self.pos_x <= coos_cible[0] and coos_cible[3] <= self.pos_y <= coos_cible[1]:
            "attaque(self,cible)"  #enlever les pvs de la cible et de l attaquant

        if self.pos_x < coos_simplifier[0]:
            self._pos_x = self.pos_x +1

        if self.pos_y < coos_simplifier[1]:
            self._pos_y = self.pos_y +1

        if self.pos_x > coos_simplifier[0]:
            self._pos_x = self.pos_x -1

        if self.pos_y > coos_simplifier[1]:
            self._pos_y = self.pos_y -1


class Arnaud(Predateur):
    def __init__(self, pos_x:int = 0, pos_y:int = 0, faim=True, couleur="#FF0000",vie=5,attaque=2, nb_a_manger = 15000):
        super().__init__(pos_x,pos_y,faim,couleur,vie,attaque,nb_a_manger)

        def se_bave_dessus():
            self.vie = 0

class Oiseau(Predateur):
    def __init__(self, pos_x:int = 0, pos_y:int = 0, faim=True, couleur="#FF0000",vie=5,attaque=2, nb_a_manger = 15000, cible = "fourmies"):
        super().__init__(pos_x,pos_y,faim,couleur,vie,attaque,nb_a_manger,cible)
        self.couleur = "blue"
        self.taille = 15

