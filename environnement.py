import random
from nid import Nid
from fourmis import Fourmis
from source_nourriture import SourceNourriture

class Environnement:
    def __init__(self, largeur=700, hauteur=700, taille_pixel=15, nb_sources=5):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_pixel = taille_pixel
        self.nb_sources = nb_sources #nombre de sources maximales en même temps

        self.taille_grille = largeur // taille_pixel


        # Applique des phéromones de tous les types sur toute la map
        self.grille_phero = [
            [
                {
                    "nourriture": 0,
                    "danger": 0,
                    "nidification": 0
                }
                for _ in range(self.taille_grille)
            ]
            for _ in range(self.taille_grille)
        ]

        self.nid = None
        self.sources = [] # liste de toutes les sources de nourritures
        self.fourmis = [] # liste de toutes les fourmis
        self.predateurs = [] #liste de tous les prédateurs

    def ajouter_nid(self, nid):
        self.nid = nid

    def ajouter_source(self, source):
        self.sources.append(source)

    def deposer_pheromone(self, x, y, type_phero, quantite):
        # Augmente quantité phéromones sur la position
        if 0 <= x < self.taille_grille and 0 <= y < self.taille_grille:
            self.grille_phero[y][x][type_phero] += quantite

    def ajouter_fourmi(self, fourmi):
        self.fourmis.append(fourmi)

    def ajouter_predateur(self, predateur):
        self.predateurs.append(predateur)

    def evaporation(self):
        pass

    def evaporation(self):
        # retire les sources dont la quantité est nulle de la liste
        self.sources = [s for s in self.sources if s.quantite > 0]
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

    def supprimer_source(self, source):
        # Retire la source de la liste des sources de l'environnement
        if source in self.sources:
            self.sources.remove(source)
            print("Source retirée de l'environnement")