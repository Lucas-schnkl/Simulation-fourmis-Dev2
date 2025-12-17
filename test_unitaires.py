import environnement
from environnement import Environnement
import fourmis
from fourmis import Fourmis
import nid
from nid import Nid
import predateur
import source_nourriture as source_nourriture
import unittest


class TestSourcceNourriture(unittest.TestCase):

    def setUp(self):                                    #fonction d'initialisation des valeurs
        self.envi = Environnement(largeur=100, hauteur=100, taille_pixel=10)
        self.source_nourriture = source_nourriture.SourceNourriture(self.envi, 0, 0, "#00FF4D", 3) #mise en place de valeur fixe

    def test_setUp(self):
        self.assertEqual(self.source_nourriture._pos_x, 0)
        self.assertEqual(self.source_nourriture._pos_y, 0)
        self.assertEqual(self.source_nourriture._couleur, "#00FF4D")
        self.assertEqual(self.source_nourriture._compteur, 3)               #verifie si la valeur mise dans setUp fonctionne (ici : "est ce que le compteur = 3?")

        self.assertIn(self.source_nourriture, source_nourriture.SourceNourriture.liste_sources)     #verifie si la classe s'est rajouté elle meme dans la liste

    def test_getter_compteur(self):
        self.assertEqual(self.source_nourriture.compteur, 3)

    def test_setter_compteur(self):
        self.source_nourriture.compteur = 1                             #va jouer compteur avec pour agr 1 donc on aura le compteur initialiser - 1
        self.assertEqual(self.source_nourriture.compteur, 2)    # rep 2 (nouv compteur)

        self.source_nourriture.compteur = 2                             # nouv compteur - 2 -> déclenche regenerer()
        # On vérifie que le compteur est maintenant une valeur de régénération (entre 5 et 15)
        self.assertTrue(5 <= self.source_nourriture.compteur <= 15)

    def test_disparaitre(self):
        self.source_nourriture.disparaitre()                    #appel la fonction de suppression
        self.assertNotIn(self.source_nourriture, source_nourriture.SourceNourriture.liste_sources)  #verifie si la class n'y est plus


class TestFourmis(unittest.TestCase):

    def setUp(self):
        # Initialisation d'un environnement de test 10x10 (100px / 10px taille_pixel)
        self.env = Environnement(largeur=100, hauteur=100, taille_pixel=10)
        self.nid = Nid(envi=self.env, pos_x=5, pos_y=5)
        self.env.ajouter_nid(self.nid)
        # Création d'une fourmi standard au centre
        self.fourmi = Fourmis(pos_x=5, pos_y=5, pheromones="")

    def test_verifier_limites(self):
        # Test que la fourmi ne sort pas de la grille (0-9 pour une grille de 10)
        # Test limite supérieure (doit être ramené à largeur_grille - 1 = 9)
        self.fourmi.pos_x = 15
        self.fourmi.pos_y = 15
        self.fourmi.verifier_limites(self.env)
        self.assertEqual(self.fourmi.pos_x, 9)
        self.assertEqual(self.fourmi.pos_y, 9)

        # Test limite inférieure (doit être ramené à 0)
        self.fourmi.pos_x = -5
        self.fourmi.pos_y = -5
        self.fourmi.verifier_limites(self.env)
        self.assertEqual(self.fourmi.pos_x, 0)
        self.assertEqual(self.fourmi.pos_y, 0)

    def test_depot_nourriture_au_nid(self):
        # Test que la nourriture est bien ajoutée au nid quand la fourmi arrive
        self.fourmi.pos_x = 5
        self.fourmi.pos_y = 5
        self.fourmi.retour = True  # La fourmi porte de la nourriture

        quantite_initiale = self.nid.quantite_nourriture
        self.fourmi.retourner_au_nid(self.env)

        # Vérifie que la nourriture du nid a augmenté de 1
        self.assertEqual(self.nid.quantite_nourriture, quantite_initiale + 1)
        # Vérifie que la fourmi n'est plus en mode retour
        self.assertFalse(self.fourmi.retour)

class TestEnvironnement(unittest.TestCase):

    def setUp(self):
        self.env = Environnement(largeur=100, hauteur=100, taille_pixel=10, nb_sources=3)

    def test_ajouter_source(self):
        s = source_nourriture.SourceNourriture(self.env, pos_x=5, pos_y=5)
        self.env.ajouter_source(s)
        self.assertIn(s, self.env.sources)

    def test_deposer_pheromone(self):
        self.env.deposer_pheromone(2, 3, "nourriture", quantite=50)
        self.assertEqual(self.env.grille_phero[3][2]["nourriture"], 50)

    def test_evaporation(self):
        self.env.deposer_pheromone(1, 1, "nourriture", quantite=50)
        self.env.evaporation()
        self.assertTrue(self.env.grille_phero[1][1]["nourriture"] <= 50)

    def test_generateur_sources_actives(self):
        s1 = source_nourriture.SourceNourriture(self.env, 0, 0, compteur=5)
        s2 = source_nourriture.SourceNourriture(self.env, 1, 1, compteur=0)
        self.env.sources = [s1, s2]
        sources_actives = list(self.env.generateur_sources_actives())
        self.assertIn(s1, sources_actives)
        self.assertNotIn(s2, sources_actives)


class TestNid(unittest.TestCase):

    def setUp(self):
        # Création d'un petit environnement réel
        self.env = Environnement(largeur=10, hauteur=10, taille_pixel=1)
        # Création d'un nid au centre
        self.nid = Nid(envi=self.env, pos_x=5, pos_y=5, quantite_nourriture=10)
        self.env.ajouter_nid(self.nid)

    def test_creation_nid(self):
        self.assertEqual(self.nid.pos_x, 5)
        self.assertEqual(self.nid.pos_y, 5)
        self.assertEqual(self.nid.quantite_nourriture, 10)
        self.assertIn((5, 5), self.nid.cases)

    def test_ajouter_nourriture(self):
        self.nid.ajouter_nourriture(5)
        self.assertEqual(self.nid.quantite_nourriture, 15)

    def test_consommer_nourriture_suffisante(self):
        result = self.nid.consommer_nourriture(5)
        self.assertTrue(result)
        self.assertEqual(self.nid.quantite_nourriture, 5)

    def test_consommer_nourriture_insuffisante(self):
        result = self.nid.consommer_nourriture(20)
        self.assertFalse(result)
        self.assertEqual(self.nid.quantite_nourriture, 10)

    def test_cases_voisines(self):
        voisins = self.nid.cases_voisines()
        # Les cases voisines du centre (5,5) dans une grille 10x10
        expected_voisins = {(4,5), (6,5), (5,4), (5,6)}
        self.assertEqual(voisins, expected_voisins)

    def test_agrandir(self):
        # On agrandit le nid
        old_len = len(self.nid.cases)
        self.nid.agrandir()
        self.assertEqual(len(self.nid.cases), old_len + 1)
        # Vérifie que la phéromone de nidification est déposée
        nouvelle_case = list(self.nid.cases - {(5,5)})[0]
        self.assertEqual(self.env.grille_phero[nouvelle_case[1]][nouvelle_case[0]]["nidification"], 100)


if __name__ == '__main__':
    unittest.main()
