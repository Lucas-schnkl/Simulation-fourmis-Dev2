import random


class SourceNourriture:
    liste_sources = []

    def __init__(self, envi, pos_x: int, pos_y: int, couleur="#00FF4D", compteur=5):
        self._envi = envi
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._couleur = couleur
        self._compteur = compteur

        # Ajout à la liste statique de la classe
        SourceNourriture.liste_sources.append(self)

    def __repr__(self):
        return f"SourceNourriture(pos_x={self._pos_x}, pos_y={self._pos_y}, compteur={self._compteur})"

    @property
    def compteur(self):
        return self._compteur

    @compteur.setter
    def compteur(self, nombre):
        self._compteur -= nombre

        if self._compteur <= 0:
            self._compteur = 0
            print('La source est vide')

            # 1. Nettoyage de la zone autour de la source
            self._envi.nettoyer_pheromones(self._pos_x, self._pos_y, rayon=6, type_phero="nourriture")

            # 2. Nettoyage du chemin retour vers le nid (ligne large)
            if self._envi.nid:
                self._envi.supprimer_piste(self._pos_x, self._pos_y, self._envi.nid.pos_x, self._envi.nid.pos_y)

            self.regenerer()

    def regenerer(self):
        # Déplace la source à un nouvel endroit aléatoire et la remplit
        largeur_max = self._envi.largeur_grille
        hauteur_max = self._envi.hauteur_grille

        while True:
            nx = random.randint(0, largeur_max - 1)
            ny = random.randint(0, hauteur_max - 1)

            # vérif pas sur le nid
            if self._envi.nid:
                if nx == self._envi.nid.pos_x and ny == self._envi.nid.pos_y:
                    continue  # On recommence si c'est sur le nid

            self._pos_x = nx
            self._pos_y = ny
            break

        # remplit la source
        self._compteur = random.randint(5, 15)
        # print(f"Source régénérée en {self._pos_x}, {self._pos_y}")

    def disparaitre(self):
        # On retire la source de la liste globale SÉCUR
        if self in SourceNourriture.liste_sources:
            SourceNourriture.liste_sources.remove(self)

        # On retire la source de l'environnement pour que les fourmis arrêtent de la voir
        if self._envi and self in self._envi.sources:
            self._envi.supprimer_source(self)