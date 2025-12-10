class Nid:
    def __init__(self, envi, pos_x: int,pos_y: int, couleur = "#ff7f00", quantite_nourriture = 0):
        self._envi = envi
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._couleur = couleur
        self._quantite_nourriture = quantite_nourriture

    def __repr__(self):
        return f"Nid({self._quantite_nourriture})"

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, nouvelle_couleur):
        self.couleur = nouvelle_couleur

    @property
    def quantite_nourriture(self):
        return self._quantite_nourriture

    def ajouter_nourriture(self, quantite: int):
        # Ajoute nourriture dans la réserve
        self._quantite_nourriture += quantite
        print(f"Quantité ajoutée : {quantite} ({self._quantite_nourriture})")
