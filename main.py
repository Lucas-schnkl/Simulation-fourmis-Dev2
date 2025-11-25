from environnement import Environnement
from simulation import Simulation
from Nid_fichier import Nid
from fourmis import Ouvriere, Soldat, Reine
from prédateurs import Predateur
from source_nourriture import SourceNourriture
from interface_graphique import InterfaceGraphique

def main():
    # Création environnement
    env = Environnement(largeur=100, hauteur=100)

    #Création interface graphique
    interface = InterfaceGraphique(env)

    # Création du nid
    nid = Nid(50, 50)
    env.ajouter_nid(nid)

    # Ajouter fourmis
    for _ in range(50):
        env.ajouter_fourmi(Ouvriere(vie=100, pos_x=50, pos_y=50, pheromones="", statut="vivante", nourriture=100))

    env.ajouter_fourmi(Reine(vie=100, statut="vivante", pheromones="", pos_x=50, pos_y=50, nourriture=100))
    env.ajouter_fourmi(Soldat(pos_x=50, pos_y=50))

    # Ajouter sources nourriture
    env.ajouter_source(SourceNourriture(10, 20, quantite=200))

    # Ajouter prédateurs
    env.ajouter_predateur(Predateur(pos_x=70, pos_y=70))

    # Lancer simulation
    sim = Simulation(env,interface)
    sim.boucle()

if __name__ == "__main__":
    main()