#class sources nourriture
class SourceNourriture:
    def __init__(self, pos_x:int, pos_y:int, statut:str="plein",quantite:int=250, couleur="#00FF4D"):
        self._quantite = quantite
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._statut = statut
        self._couleur = couleur

    #définit quantite de nourriture restante
    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self,x):
        self._quantite = x

    #diminue quantite de nourriture restante quand fourmis
    #viennent en chercher
    def perd_nourriture(self,x):
        self.quantite -= x
        if self._quantite <= 0:
            self._quantite = 0
            self.statut = "vide"

    #définit si source est vide ou non
    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self,x):
        self._statut = x

    #définit position de la source
    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self,x):
        self._pos_x = x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y):
        self._pos_y = y


    def disparaitre(self):
        pass
        #si source vide, faire disparaitre de la carte ?

    """générer source de temps en temps dans un autre fichier ?"""
