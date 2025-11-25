import random
from nid import Nid
from fourmis import Fourmis, Pheromones
from source_nourriture import SourceNourriture

class Environnement:
    def __init__(self, largeur=700, hauteur=700, taille_pixel=15, nb_sources=5):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_pixel = taille_pixel
        self.nb_sources = nb_sources #nombre de sources maximales en même temps

        self.taille_grille = largeur // taille_pixel

        self.grille_phero = [
            [Pheromones() for _ in range(self.taille_grille)]
            for _ in range(self.taille_grille)
        ]

        self.nid = None
        self.sources = []
        self.fourmis = []
        self.predateurs = []

    def ajouter_nid(self, nid):
        self.nid = nid

    def ajouter_source(self, source):
        self.sources.append(source)

    def ajouter_fourmi(self, fourmi):
        self.fourmis.append(fourmi)

    def ajouter_predateur(self, predateur):
        self.predateurs.append(predateur)

    def evaporation(self):
        pass

    def generer_sources(self):
        # génère source de nourriture à position aléatoire
        for _ in range(self.nb_sources):
            while True:
                # prends x et y au hasard (de 0 à taille max de la grille)
                x = random.randint(0, self.taille_grille - 1)
                y = random.randint(0, self.taille_grille - 1)

                # vérifie que position choisie est pas celle du nid
                if not self.nid or (x, y) != (self.nid.pos_x, self.nid.pos_y):
                    break

            self.sources.append(SourceNourriture(pos_x=x, pos_y=y))
