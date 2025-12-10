class SourceNourriture:
    liste_sources = []
    def __init__(self, envi, pos_x: int, pos_y: int, couleur="#00FF4D", compteur=3):
        self._envi = envi
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._couleur = couleur
        self._compteur = compteur

    def __repr__(self):
        return f"Sources({self.liste_sources}')"

    @property
    def compteur(self):
        # Définit le nombre de fois que fourmis
        # peuvent prendre nourriture avant que soit vide
        return self._compteur

    @compteur.setter
    def compteur(self, nombre):
        self._compteur -= nombre
        if self._compteur <= 0:
            self._compteur = 0

            print('La source est vide')
            self.disparaitre()

    def disparaitre(self):
        # Supprime la source si le compteur <= 0
        self._envi.source.supprimer_source(self)