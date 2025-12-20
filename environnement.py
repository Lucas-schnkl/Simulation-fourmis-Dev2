import random
from source_nourriture import SourceNourriture


class Environnement:
    limiter_a_zero = lambda self, v: max(0, v)

    def __init__(self, largeur=1200, hauteur=750, taille_pixel=10, nb_sources=5):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_pixel = taille_pixel
        self.nb_sources = nb_sources

        self.largeur_grille = largeur // taille_pixel
        self.hauteur_grille = hauteur // taille_pixel

        # NOUVEAU : Compteur pour le nettoyage global
        self.compteur_sans_manger = 0
        self.seuil_nettoyage = 200  # Après 500 ticks sans manger, on nettoie tout

        # Initialisation de la grille
        self.grille_phero = []
        for y in range(self.hauteur_grille):
            ligne = []
            for x in range(self.largeur_grille):
                ligne.append({
                    "nourriture": 0,
                    "danger": 0,
                    "nidification": 0
                })
            self.grille_phero.append(ligne)

        self.nid = None
        self.sources = []
        self.fourmis = []
        self.predateurs = []
        self.larves = []

    def ajouter_nid(self, nouveau_nid):
        self.nid = nouveau_nid

    def ajouter_source(self, source):
        self.sources.append(source)

    def ajouter_larve(self, larve):
        self.larves.append(larve)

    def nettoyer(self):
        # Supprime les sources vides
        self.sources = list(filter(lambda s: s.compteur > 0, self.sources))
        print(f"nombre de sources : {len(self.sources)}")

        # Supprime les fourmis mortes
        self.fourmis = list(filter(lambda f: f.vivante, self.fourmis))

    # Appelée par le nid quand une fourmi ramène à manger
    def signal_nourriture_apportee(self):
        self.compteur_sans_manger = 0

    def deposer_pheromone(self, x, y, type_phero, quantite=100):
        # Bloque le dépôt sur le nid
        if type_phero == "nourriture" and self.nid:
            if (x, y) in self.nid.cases:
                return

        if 0 <= x < self.largeur_grille and 0 <= y < self.hauteur_grille:
            self.grille_phero[y][x][type_phero] += quantite
            if self.grille_phero[y][x][type_phero] > 100:
                self.grille_phero[y][x][type_phero] = 100

    def nettoyer_pheromones(self, x, y, rayon, type_phero):
        for dy in range(-rayon, rayon + 1):
            for dx in range(-rayon, rayon + 1):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.largeur_grille and 0 <= ny < self.hauteur_grille:
                    self.grille_phero[ny][nx][type_phero] = 0

    # NOUVEAU : Fonction radicale pour tout nettoyer
    def nettoyer_toutes_pheromones_nourriture(self):
        print("--- NETTOYAGE GLOBAL DES PISTES (FAMINE) ---")
        for y in range(self.hauteur_grille):
            for x in range(self.largeur_grille):
                self.grille_phero[y][x]["nourriture"] = 0

    def supprimer_piste(self, x1, y1, x2, y2):
        dist_x = x2 - x1
        dist_y = y2 - y1
        steps = max(abs(dist_x), abs(dist_y))

        if steps == 0: return

        dx = dist_x / steps
        dy = dist_y / steps

        curr_x = float(x1)
        curr_y = float(y1)

        for _ in range(int(steps)):
            self.nettoyer_pheromones(int(curr_x), int(curr_y), rayon=4, type_phero="nourriture")
            curr_x += dx
            curr_y += dy

    def ajouter_fourmi(self, fourmi):
        self.fourmis.append(fourmi)

    def ajouter_predateur(self, predateur):
        self.predateurs.append(predateur)

    def evaporation(self):
        # 1. Gestion du compteur de famine
        self.compteur_sans_manger += 1

        if self.compteur_sans_manger >= self.seuil_nettoyage:
            self.nettoyer_toutes_pheromones_nourriture()
            self.compteur_sans_manger = 0  # On reset après le nettoyage

        # 2. Evaporation classique
        try :
            for y in range(self.hauteur_grille):
                for x in range(self.largeur_grille):
                    case = self.grille_phero[y][x]
                    for type_phero in case:

                        case[type_phero] = self.limiter_a_zero(case[type_phero] - 10)

        except Exception as e:
            print("Simulation arrêtée :", e)

    def generer_sources(self):
        for _ in range(self.nb_sources):
            while True:
                x = random.randint(0, self.largeur_grille - 1)
                y = random.randint(0, self.hauteur_grille - 1)
                if not self.nid or (x, y) != (self.nid.pos_x, self.nid.pos_y):
                    break
            self.sources.append(SourceNourriture(self, pos_x=x, pos_y=y))

    def supprimer_source(self, source):
        if source in self.sources:
            self.sources.remove(source)

    def generateur_sources_actives(self):
        #Générateur qui renvoie uniquement les sources ayant encore de la nourriture
        for source in self.sources:
            if source.compteur > 0:
                yield source

    def fourmis_type(self, type_classe):        #cette fonction a pour but de nous renvoyer le type des fourmis
        for f in self.fourmis:
            if isinstance(f, type_classe) and f.vivante:   #On regarde si dans avec "isinstance" si f (donc une fourmie de la liste) si elle est une instance de "type_classe".
                yield f                                    #Ici yield a pour but de renvoyer une fourmis qui correspont aux critères dès qu'elle en trouve un.
                                                           #Avec une liste classique, on aurait du attendre que tout se remplisse avant de pouvoir envoyer → yield = economie de perf.

    def predateurs_actifs(self):
        # Renvoie tous les prédateurs dans la liste qui ne sont pas en fuite
        for preda in self.predateurs:
            if not preda._fuite:
                yield preda
