import math
import random
from nid import Nid


class Fourmis:
    def __init__(self, pos_x: int, pos_y: int, pheromones: str, retour: bool = False, couleur="#000000",
                 vivante: bool = True):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._pheromones = pheromones
        self._retour = retour
        self._couleur = couleur
        self._vivante = vivante

        # Mémoire pour éviter les demi-tours immédiats
        self.derniere_pos = None

        # --- Les Properties ---

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x):
        self._pos_x = x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y):
        self._pos_y = y

    @property
    def pheromones(self):
        return self._pheromones

    @pheromones.setter
    def pheromones(self, type_phero):
        self._pheromones = type_phero

    @property
    def retour(self):
        return self._retour

    @retour.setter
    def retour(self, x):
        self._retour = x

    @property
    def couleur(self):
        return self._couleur

    @couleur.setter
    def couleur(self, new_couleur):
        self._couleur = new_couleur

    @property
    def vivante(self):
        return self._vivante

    @vivante.setter
    def vivante(self, etat: bool):
        self._vivante = etat
        if not etat:
            self.mort()

    def __str__(self):
        return f"{self._pos_x},{self._pos_y} {self._retour} {self._pheromones} {self._couleur} {self._vivante} "

    def mort(self):
        self._vivante = False

    def nidifier(self):
        pass

    def verifier_limites(self, env):
        """Sécurité : empêche de sortir de la grille"""
        if self.pos_x < 0: self.pos_x = 0
        if self.pos_x >= env.largeur_grille: self.pos_x = env.largeur_grille - 1
        if self.pos_y < 0: self.pos_y = 0
        if self.pos_y >= env.hauteur_grille: self.pos_y = env.hauteur_grille - 1

    def se_deplacer(self, env):
        # AJOUT : Bloc Try-Except pour la robustesse (Gestion des erreurs)
        try:
            if not self._vivante:
                return

            pos_actuelle_x = self.pos_x
            pos_actuelle_y = self.pos_y

            # 1. RETOUR AU NID
            if self._retour:
                self.retourner_au_nid(env)
                self.verifier_limites(env)
                self.derniere_pos = None
                return

            # 2. RECHERCHE NOURRITURE (Vue directe)
            source_proche = None
            dist_min = 6

            for source in env.sources:
                d = math.sqrt((self.pos_x - source._pos_x) ** 2 + (self.pos_y - source._pos_y) ** 2)
                if d <= 5 and d < dist_min:
                    dist_min = d
                    source_proche = source

            if source_proche:
                self._aller_vers_cible(source_proche._pos_x, source_proche._pos_y)
                if dist_min <= 1:
                    source_proche.compteur = 1
                    self.retour = True
                    self.retourner_au_nid(env)

                self.verifier_limites(env)
                self.derniere_pos = None
                return

            # 3. EXPLORATION
            meilleur_dx, meilleur_dy = 0, 0
            meilleur_score = -float('inf')

            voisins = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            random.shuffle(voisins)

            mouvement_trouve = False

            # --- SOLUTION ANTI-BLOCAGE ---
            dist_nid = 9999
            if env.nid:
                dist_nid = math.sqrt((self.pos_x - env.nid.pos_x) ** 2 + (self.pos_y - env.nid.pos_y) ** 2)

            aveugle_nourriture = (dist_nid < 15)

            for dx, dy in voisins:
                nx = self.pos_x + dx
                ny = self.pos_y + dy

                if 0 <= nx < env.largeur_grille and 0 <= ny < env.hauteur_grille:

                    score = random.uniform(0, 1)

                    phero_nourriture = env.grille_phero[ny][nx]["nourriture"]
                    phero_danger = env.grille_phero[ny][nx]["danger"]

                    # Si on n'est pas aveugle, on suit la nourriture
                    if not aveugle_nourriture:
                        if phero_nourriture > 0:
                            score += phero_nourriture + 10

                    # On fuit toujours le danger
                    if phero_danger > 0:
                        score -= (phero_danger * 100)

                    # Si on est proche du nid (aveugle), on favorise légèrement l'éloignement du centre
                    if aveugle_nourriture and env.nid:
                        dist_future = math.sqrt((nx - env.nid.pos_x) ** 2 + (ny - env.nid.pos_y) ** 2)
                        if dist_future > dist_nid:
                            score += 2

                    # Pénalité mémoire
                    if self.derniere_pos == (nx, ny):
                        score -= 50

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_dx, meilleur_dy = dx, dy
                        mouvement_trouve = True

            if mouvement_trouve:
                self.pos_x += meilleur_dx
                self.pos_y += meilleur_dy
                self.derniere_pos = (pos_actuelle_x, pos_actuelle_y)

            self.verifier_limites(env)

        except Exception as e:
            # En cas d'erreur, on l'affiche mais la simulation continue
            print(f"Erreur critique sur la fourmi {self} : {e}")
            self.mort()  # Optionnel : on tue la fourmi buguée pour éviter qu'elle ne spamme l'erreur

    def _aller_vers_cible(self, tx, ty):
        if self.pos_x < tx:
            self.pos_x += 1
        elif self.pos_x > tx:
            self.pos_x -= 1
        if self.pos_y < ty:
            self.pos_y += 1
        elif self.pos_y > ty:
            self.pos_y -= 1

    def retourner_au_nid(self, env):
        nid = env.nid
        nid_x = nid.pos_x
        nid_y = nid.pos_y

        if self._pos_x < nid_x:
            self._pos_x += 1
        elif self._pos_x > nid_x:
            self._pos_x -= 1

        if self._pos_y < nid_y:
            self._pos_y += 1
        elif self._pos_y > nid_y:
            self._pos_y -= 1

        self.verifier_limites(env)

        sur_le_nid = (self._pos_x, self._pos_y) in nid.cases

        if not sur_le_nid:
            env.deposer_pheromone(self._pos_x, self._pos_y, "nourriture")

        if self._pos_x == nid_x and self._pos_y == nid_y:
            nid.ajouter_nourriture(1)
            self._retour = False


class Soldat(Fourmis):
    liste_soldats = []

    def __init__(self, pos_x: int, pos_y: int, pheromones: str = "aucun", retour: bool = False, couleur="#0000FF",
                 vivante: bool = True):
        super().__init__(pos_x, pos_y, pheromones, retour, couleur, vivante)
        Soldat.liste_soldats.append(self)

    def __repr__(self):
        return f"Soldat(x={self.pos_x}, y={self.pos_y})"

    def deposer_pheromones_danger(self, env):
        if not self.vivante: return
        rayon = 2
        for dy in range(-rayon, rayon + 1):
            for dx in range(-rayon, rayon + 1):
                tx = self.pos_x + dx
                ty = self.pos_y + dy
                if 0 <= tx < env.largeur_grille and 0 <= ty < env.hauteur_grille:
                    env.deposer_pheromone(tx, ty, "danger", 100)

    def se_deplacer(self, env):
        try:
            if not self._vivante:
                return

            pos_actuelle_x = self.pos_x
            pos_actuelle_y = self.pos_y

            # 1. EXPLORATION ET DEFENSE (Le soldat ne cherche plus de nourriture)
            meilleur_dx, meilleur_dy = 0, 0
            meilleur_score = -float('inf')

            voisins = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
            random.shuffle(voisins)

            mouvement_trouve = False

            # Calcul de la distance au nid pour l'anti-blocage
            dist_nid = 9999
            if env.nid:
                dist_nid = math.sqrt((self.pos_x - env.nid.pos_x)**2 + (self.pos_y - env.nid.pos_y)**2)

            for dx, dy in voisins:
                nx = self.pos_x + dx
                ny = self.pos_y + dy

                if 0 <= nx < env.largeur_grille and 0 <= ny < env.hauteur_grille:
                    score = random.uniform(0, 1)

                    phero_danger = env.grille_phero[ny][nx]["danger"]

                    # LE SOLDAT EST ATTIRÉ PAR LE DANGER (au lieu de le fuir)
                    if phero_danger > 0:
                        score += phero_danger * 50

                    # Favorise l'éloignement du nid s'il est trop proche
                    if dist_nid < 15 and env.nid:
                        dist_future = math.sqrt((nx - env.nid.pos_x)**2 + (ny - env.nid.pos_y)**2)
                        if dist_future > dist_nid:
                            score += 2

                    # Pénalité mémoire pour éviter les allers-retours
                    if self.derniere_pos == (nx, ny):
                        score -= 50

                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_dx, meilleur_dy = dx, dy
                        mouvement_trouve = True

            if mouvement_trouve:
                self.pos_x += meilleur_dx
                self.pos_y += meilleur_dy
                self.derniere_pos = (pos_actuelle_x, pos_actuelle_y)

            self.verifier_limites(env)

        except Exception as e:
            print(f"Erreur critique sur le soldat {self} : {e}")
            self.mort()


class Reine(Fourmis):
    def __init__(self, pos_x: int, pos_y: int, pheromones: str = "aucun", retour: bool = False, couleur="#FFD700",
                 vivante: bool = True):
        super().__init__(pos_x, pos_y, pheromones, retour, couleur, vivante)

    def __repr__(self):
        return f"Reine(x={self.pos_x}, y={self.pos_y})"

    def se_deplacer(self, env):
        if not self.vivante: return
        if env.nid:
            self.pos_x = env.nid.pos_x
            self.pos_y = env.nid.pos_y

            COUT_AGRANDI = 10
            if env.nid.quantite_nourriture >= COUT_AGRANDI:
                agrandir_nid = env.nid.consommer_nourriture(COUT_AGRANDI)
                if agrandir_nid:
                    env.nid.agrandir()
                    env.deposer_pheromone(self.pos_x, self.pos_y, "nidification", 100)


class Larve:
    def __init__(self):
        # Temps en "ticks" avant de devenir une fourmi (ex: 50 tours)
        self.temps_eclosion = 50

    def grandir(self):
        # Diminue le temps restant. Retourne True si prête à éclore.
        self.temps_eclosion -= 1
        return self.temps_eclosion <= 0