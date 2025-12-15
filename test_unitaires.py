import environnement
import fourmis
import nid
import predateur
import source_nourriture as source_nourriture
import unittest

class TestSourcceNourriture(unittest.TestCase):

    def setUp(self):                                    #fonction d'initialisation des valeurs
        self.envi = environnement.Environnement()
        self.source_nourriture = source_nourriture.SourceNourriture(self.envi,0,0,"#00FF4D",3) #mise en place de valeur fixe

    def test_setUp(self):
        self.assertEqual(self.source_nourriture._pos_x, 0)
        self.assertEqual(self.source_nourriture._pos_y, 0)
        self.assertEqual(self.source_nourriture._couleur, "#00FF4D")
        self.assertEqual(self.source_nourriture._compteur, 3)               #verifie si la valeur mise dans setUp fonctionne (ici : "est ce que le compteur = 3?")

        self.assertIn(self.source_nourriture, source_nourriture.SourceNourriture.liste_sources)     #verifie si la classe s'est rajouté elle meme dans la liste

    def test_getter_compteur(self):
        self.assertEqual(self.source_nourriture._compteur, 3)

    def test_setter_compteur(self):
        self.source_nourriture.compteur = 1                             #va jouer compteur avec pour agr 1 donc on aura le compteur initialiser - 1
        self.assertEqual(self.source_nourriture.compteur, 2)    # rep 2 (nouv compteur)

        self.source_nourriture.compteur = 2                             # nouv compteur - 2
        self.assertEqual(self.source_nourriture.compteur, 0)    # rep 0

    def test_disparaitre(self):
        self.source_nourriture.disparaitre()                    #appel la fonction
        self.assertNotIn(self.source_nourriture, source_nourriture.SourceNourriture.liste_sources)  #verifie si la class s'y trouve