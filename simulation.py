class Simulation:
    def __init__(self, environnement, interface):
        self.env = environnement
        self.en_cours = True
        self._interface = interface

    def boucle(self):
        self._interface.dessiner_static()
        while self.en_cours:
            # Déplacement fourmis
            for f in self.env.fourmis:
                # boucle sur chaque fourmis pour qu'elle trouve de la nourriture (déplacement)
                f.se_deplacer()
                self._interface.update()

            # boucle sur chaque prédateur pour chasse (déplacement)
            for p in self.env.predateurs:
                p.chasser()
                self._interface.update()

            # Evaporation phéromones
            self.env.evaporation()
            self._interface.update()

            # Mise à jour du nid
            if self.env.nid:
                self.env.nid.cycle_interne()
                self._interface.update()

"""Faire appels de temps en pour ajouter prédateurs et autres sources ?"""
