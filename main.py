from environnement import Environnement
from nid import Nid
from source_nourriture import SourceNourriture
from predateur import Predateur
from simulation import Simulation
from fourmis import Fourmis
import random


# Création environnement
env = Environnement(largeur=100, hauteur=100)

def main():
    # Création du nid
    nid = Nid(envi=env, pos_x=50, pos_y=50)
    env.ajouter_nid(nid)

    # Ajouter fourmis
    for _ in range(50):
        env.ajouter_fourmi(Fourmis(envi = env,pos_x=50, pos_y=50, pheromones=""))

    #env.ajouter_fourmi(Reine(envi = env, vie=100, statut="vivante", pheromones="", pos_x=40, pos_y=40, nourriture=100))
    #env.ajouter_fourmi(Soldat(envi = env, pos_x=55, pos_y=55))

    # Ajouter sources nourriture
    nbr_sources = 5
    taille_env = 100

    for _ in range(nbr_sources):
        while True:
            x = random.randint(0, taille_env - 1)
            y = random.randint(0, taille_env - 1)

            if (x, y) != (30, 30): # spawn pas sur le nid
                break

        env.ajouter_source(SourceNourriture(envi=env, pos_x=x, pos_y=y, compteur=3))

    # Ajouter prédateurs
    env.ajouter_predateur(Predateur(envi=env, pos_x=70, pos_y=70))

    # Lancer simulation
    sim = Simulation(env)
    sim.boucle()

    # garde la fenêtre de la simulation ouverte
    #interface.fenetre.mainloop()


if __name__ == "__main__":
    main()
