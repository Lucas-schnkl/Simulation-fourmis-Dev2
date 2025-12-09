from environnement import Environnement
from simulation import Simulation
from nid import Nid
from fourmis import Ouvriere, Soldat, Reine
from prédateurs import Predateur
from source_nourriture import SourceNourriture
from interface_graphique import InterfaceGraphique
import random


# Création environnement
env = Environnement(largeur=100, hauteur=100)

def main():
    #Création interface graphique
    interface = InterfaceGraphique(env)

    # Création du nid
    nid = Nid(30, 30)
    env.ajouter_nid(nid)

    # Ajouter fourmis
    for _ in range(50):
        env.ajouter_fourmi(Ouvriere(envi = env, vie=100, pos_x=50, pos_y=50, pheromones="", statut="vivante", nourriture=100))
        """Mettre positions de départ différentes"""

    env.ajouter_fourmi(Reine(envi = env, vie=100, statut="vivante", pheromones="", pos_x=40, pos_y=40, nourriture=100))
    env.ajouter_fourmi(Soldat(envi = env, pos_x=55, pos_y=55))

    # Ajouter sources nourriture
    nbr_sources = 5
    taille_env = 100

    for _ in range(nbr_sources):
        while True:
            x = random.randint(0, taille_env - 1)
            y = random.randint(0, taille_env - 1)

            if (x, y) != (30, 30): # spawn pas sur le nid
                break

        env.ajouter_source(SourceNourriture(x, y, quantite=200))

    # Ajouter prédateurs
    env.ajouter_predateur(Predateur(pos_x=70, pos_y=70))

    # Lancer simulation
    sim = Simulation(env,interface)
    sim.boucle()

    # garde la fenêtre de la simulation ouverte
    interface.fenetre.mainloop()


if __name__ == "__main__":
    main()
