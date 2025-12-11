class Simulation:
    def __init__(self, environnement):
        self.env = environnement
        self.en_cours = True
        #self._interface = interface

    # Boucle infinie pour la simulation
    def boucle(self):
        while self.en_cours:
            if not self.en_cours:
                return

            # dessin état statique
            #self._interface.dessiner_static()

            # dessin sources de nourriture
            #self._interface.dessiner_sources()

            # déplacement fourmis
            for f in self.env.fourmis:
                f.se_deplacer(self.env)
                #f.trouve_nourriture(self.env.sources)

            # déplacement prédateurs
            for p in self.env.predateurs:
                p.se_deplacer()

            # evaporation
            #self.env.evaporation()

            # update interface
            #self._interface.update()

            # relancer la boucle dans 30 ms acr tkinter aime pas boucle infini donc fait équivalent
            #self._interface.fenetre.after(30, self.boucle)

            print("Une boucle de la simulation a tourné")
