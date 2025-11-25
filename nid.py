import random


class Nid:
    def __init__(self, pos_x: int,pos_y: int, couleur = "#000000", taille : int = 20, capacite: int = 500):
        # Position du nid
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._couleur = couleur # son affichage dans la map
        self._taille = taille
        self._capacite = capacite  # nombre max de fourmis par nid

        # parites internes
        self._salle_ponte = []  #  les œufs et la Reine
        self._salle_larves = []  #  les larves en développement
        self._reserve_nourriture = 0  # stock nourriture
        self._salle_defense = []  #  les soldats
        self._salle_entretien = []  # ouvrières à l’intérieur

        # Stat
        self._total_oeufs = 0
        self._total_larves = 0
        self._total_fourmis = 0

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
    def couleur(self, couleur):
        self.couleur = couleur

    @property
    def reserve_nourriture(self):
        return self._reserve_nourriture

    @reserve_nourriture.setter
    def reserve_nourriture(self, valeur):
        self._reserve_nourriture = max(0, valeur)

    @property
    def capacite(self):
        return self._capacite

    @property
    def total_fourmis(self):
        return self._total_fourmis

    def ajouter_nourriture(self, quantite: int):
        # Ajoute nourriture dans la réserve
        self._reserve_nourriture += quantite
        print(f"Quantité ajoutée : {quantite} ({self._reserve_nourriture})")

    def consommer_nourriture(self, quantite: int):
        # Consommation nid (larves + fourmis)
        if self._reserve_nourriture >= quantite:
            self._reserve_nourriture -= quantite
        else:
            self._reserve_nourriture = 0
            print("Le nid est à court de nourriture")

    def ajouter_reine(self, reine):
        # Ajoute la Reine dans la salle de ponte
        self._salle_ponte.append(reine)

    def pondre_oeuf(self):
        # Ajoute un œuf
        self._total_oeufs += 1
        print(f"Œuf pondu. Total œufs = {self._total_oeufs}")

    def transformer_oeuf_en_larve(self, larve):
        # Bouge un œuf vers la salle des larves
        if self._total_oeufs > 0:
            self._total_oeufs -= 1
            self._salle_larves.append(larve)
            self._total_larves += 1
            print(f"Nouvelle larve ({self._total_larves})")

    def metmorphose_larve(self, fourmi):
        # Quand larve devient fourmi adulte
        if fourmi:
            self._salle_larves = [l for l in self._salle_larves if l.statut != "morte"]
            self._total_larves = len(self._salle_larves)
            self._total_fourmis += 1

    def affecter_soldat(self, soldat):
        # Envoie soldat dans la salle de défense
        self._salle_defense.append(soldat)
        print("Soldat affecté à la défense du nid")

    def affecter_ouvriere(self, ouvriere):
        # Ajoute ouvrière à l’entretien du nid
        self._salle_entretien.append(ouvriere)
        print(" Ouvrière affectée à l’entretien du nid")

    def cycle_interne(self):
        # Simule la vie interne du nid (consommation, développement)
        # Consommation collective de nourriture
        consommation = len(self._salle_larves) * 2 + self._total_fourmis // 5
        self.consommer_nourriture(consommation)

        # Croissance des larves
        for larve in self._salle_larves:
            larve.developpement(5)  # augmente la croissance
            if larve.croissance >= 100:
                larve.metamorphose()

        # Reproduction possible si assez de ressources
        if self._reserve_nourriture > 50 and self._salle_ponte:
            if random.random() < 0.3:  # proba de ponte
                self.pondre_oeuf()

    def etat_nid(self):
        # résumé de l’état du nid
        return {
            "position": (self._pos_x, self._pos_y),
            "nourriture": self._reserve_nourriture,
            "oeufs": self._total_oeufs,
            "larves": self._total_larves,
            "fourmis_adultes": self._total_fourmis,
            "soldats": len(self._salle_defense),
            "ouvrieres": len(self._salle_entretien)
        }

    @property
    def taille(self):
        return self._taille

#nid = Nid(10, 20)
#nid.ajouter_reine(reine)
#nid.cycle_interne()
#ajouter_nourriture()   # quand les ouvrières rapportent à manger
#consommer_nourriture() # quand les larves et fourmis mangent
#print(nid.etat_nid())
