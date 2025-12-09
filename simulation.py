import random

class Simulation:
    def __init__(self, environnement, interface):
        self.env = environnement
        self.en_cours = True
        self._interface = interface

    def boucle(self):
        if not self.en_cours:
            return

        # dessin état statique
        #self._interface.dessiner_sources() ,il est dans le main mtn

        # dessin sources de nourriture
        self._interface.dessiner_sources()

        # déplacement fourmis
        for f in self.env.fourmis:
            f.se_deplacer(self.env)
            if not f.mode_retour:
                f.trouve_nourriture(self.env.sources)

        # déplacement prédateurs
        for p in self.env.predateurs:
            p.chasser()

        # evaporation
        self.env.evaporation()

        # update interface
        self._interface.update()

        # relancer la boucle dans 30 ms acr tkinter aime pas boucle infini donc fait équivalent
        self._interface.fenetre.after(30, self.boucle)


"""ajouter prédateurs et autres sources de temps en temps"""
