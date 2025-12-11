import math
import random

class Fourmis:
    def __init__(self, pos_x:int, pos_y:int, pheromones: str, retour:bool=False, couleur="#000000", vivante:bool=True):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pheromones = pheromones
        self._retour = retour
        self._couleur = couleur
        self._vivante = vivante

    # --- Les Properties ---
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
    def pos_y(self,y):
        self._pos_y = y

    @property
    def pheromones(self):
        return self._pheromones

    @pheromones.setter
    def pheromones(self,type_phero):
        self._pheromones = type_phero

    @property
    def retour(self):
        return self._retour

    @retour.setter
    def retour(self,x):
        self._retour = x

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self,new_couleur):
        self._couleur = new_couleur

    @property
    def vivante(self): return self._vivante

    @vivante.setter
    def vivante(self,etat: bool):
        self._vivante = etat
        if not etat:
            self.mort()

    def __str__(self):
        return f"{self._pos_x},{self._pos_y} {self._retour} {self._pheromones} {self._couleur} {self._vivante} "

    def mort(self):
        #fourmi comme non vivante.
        self._vivante = False

    def nidifier(self):
        #agrandire case nid
        pass

    def se_deplacer(self, env):
        #deplacer la fourmi dans l'environnement
        if not self._vivante:
            return
        #deplacer la fourmi vers le nid
        if self._retour:
            self.retourner_au_nid(env)
            return
        #Mode Explo
        #Détect NOURRITURE
        source_proche = None
        dist_min = 6 #5 pixel de range

        for source in env.sources:
            #utilise _pos_x car SourceNourriture a pas de property pos_x
            d = math.sqrt((self.pos_x - source.pos_x)**2 + (self.pos_y - source.pos_y)**2)

            if d <= 5 and d < dist_min:
                dist_min = d
                source_proche = source

            if source_proche:
                self._aller_vers_cible(source_proche.pos_x, source_proche.pos_y)
                if dist_min <= 1:
                    source_proche.compteur -= 1 #la fourmis prend 1 de la source à voir comment le mettre dans source nourriture
                    self.retour = True
                    self.retourner_au_nid(env)
                return

    # DÉPLACEMENT PHÉROMONES ET ALÉATOIRE
        meilleur_dx, meilleur_dy = 0, 0
        meilleur_score = -float('inf')
    # Liste déplacements possibles (dx, dy)
        voisins = [
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1)
        ]
        random.shuffle(voisins)

        mouvement_trouve = False

        for dx, dy in voisins:
            nx = self.pos_x + dx
            ny = self.pos_y + dy

            # Vérif qu'on reste dans la grille
            if 0 <= nx < env.taille_grille and 0 <= ny < env.taille_grille:
                # Récup des phéromones
                phero_nourriture = env.grille_phero[ny][nx]["nourriture"]
                phero_danger = env.grille_phero[ny][nx]["danger"]

                #CALCUL DU SCORE DU DÉPLACEMENT
                # Score de base aléatoire
                score = random.uniform(0, 1)

                # Si nourriture le score augmente
                if phero_nourriture > 0:
                    score += phero_nourriture + 10

                # Si danger le score baisse fort
                if phero_danger > 0:
                    score -= (phero_danger * 100)

                #garde mouvement avec le meilleur score
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_dx, meilleur_dy = dx, dy
                    mouvement_trouve = True

                #déplacement
            if mouvement_trouve:
                self.pos_x += meilleur_dx
                self.pos_y += meilleur_dy

    def _aller_vers_cible(self, tx, ty): #peut etre utile pour les gardes vers le prédateur
        if self.pos_x < tx:
            self.pos_x += 1
        elif self.pos_x > tx:
            self.pos_x -= 1

        if self.pos_y < ty:
            self.pos_y += 1
        elif self.pos_y > ty:
            self.pos_y -= 1

    def retourner_au_nid(self,env):
        nid = env.nid
        #récupére position nid
        nid_x = nid.pos_x
        nid_y = nid.pos_y

        #mouvement en X (si je suis à gauche, je vais à droite)
        if self._pos_x < nid_x:
            self._pos_x += 1
        elif self._pos_x > nid_x:
            self._pos_x -= 1

        # mouvement en Y
        if self._pos_y < nid_y:
            self._pos_y += 1
        elif self._pos_y > nid_y:
            self._pos_y -= 1

        env.deposer_pheromones(self._pos_x, self._pos_y, "nourriture")

        if self._pos_x == nid_x and self._pos_y == nid_y:
            nid.ajouter_nourriture(1)
            self._retour = False

    class Soldat(Fourmis) :
        liste_soldats = []

        def __init__(self, pos_x: int, pos_y: int, pheromones: str = "aucun", retour: bool = False, couleur="#0000FF", vivante: bool = True):

            super().__init__(pos_x, pos_y, pheromones, retour, couleur, vivante)

            Soldat.liste_soldats.append(self)

        def __repr__(self):
            return f"Soldat(x={self.pos_x}, y={self.pos_y})"

        def deposer_pheromones_danger(self,env):
            pass
