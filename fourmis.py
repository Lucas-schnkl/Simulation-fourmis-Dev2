import math

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
        # (Ici code pour la recherche si retour est False)

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



