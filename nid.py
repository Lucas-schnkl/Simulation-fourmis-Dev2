import random

class Nid:
    def __init__(self, envi, pos_x: int,pos_y: int, couleur = "#ff7f00", quantite_nourriture = 0):
        self._envi = envi
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._couleur = couleur
        self._quantite_nourriture = quantite_nourriture
        self.cases = set() #listes des cases qui composent le nid (dans un set pour être sûr qu'on a pas 2 fois les mêmes)
        self.cases.add((self._pos_x, self._pos_y))

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
        #signale à l'environnement qu'on a mangé, donc pas besoin de nettoyer
        if self._envi:
            self._envi.signal_nourriture_apportee()

    def consommer_nourriture(self, quantite: int):
        if self._quantite_nourriture >= quantite:
            self._quantite_nourriture -= quantite
           # print(f"Nourriture consommée : -{quantite} (Reste: {self._quantite_nourriture})")
            return True
        return False

    def cases_voisines(self):
        voisins = set()
        for i in self.cases:
            # cases actuelles du nid
            x = i[0]
            y = i[1]
            # regardes cases voisines
            for j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                dx = j[0]
                dy = j[1]
                nx = x + dx
                ny = y + dy

                if 0 <= nx < self._envi.largeur_grille and 0 <= ny < self._envi.hauteur_grille:
                    voisins.add((nx, ny))

        # retire les cases qui font déjà partie du nid
        cases_valides = voisins - self.cases
        return cases_valides

    def agrandir(self):
        candidates = list(self.cases_voisines())
        if candidates:
            nouvelle_case = random.choice(candidates)
            self.cases.add(nouvelle_case)
            #print(f"Nid agrandi : +1 case → total = {len(self.cases)}")
            self._envi.deposer_pheromone(nouvelle_case[0], nouvelle_case[1], "nidification", 100) #depose la phero de nidification
