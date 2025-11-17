import random

#met toutes fourmis dans dico
colonie = {}
nbr_fourmis = 0

#mettre sources dans dico ?
sources = {}
nbr_source = 0

class Fourmis:
    def __init__(self,
                 chemin_retour:list = [],
                 pheromones:str="",
                 pos_x:int="",
                 pos_y:int="",
                 statut:str="vivante",
                 vie:int=100,
                 nourriture:int=100,
                 transport_nourriture:int=0,
                 capacite_transport:int=100,
                 mode_retour:bool=False,
                 ):
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._nourriture = nourriture
        self._transport_nourriture = transport_nourriture
        self._capacite_transport = capacite_transport
        self._pheromones = pheromones
        self._vie = vie
        self._statut = statut
        self._mode_retour = mode_retour
        self._chemin_retour = chemin_retour

    #phéromones
    @property
    def pheromones(self):
        return self._pheromones

    @pheromones.setter
    def pheromones(self, type):
        self._pheromones = type

    #position x
    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, x):
        self._pos_x = x

    #position y
    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self,y):
        self._pos_y = y

    #statut (mort ou vivant)
    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, x):
        self._statut = x

    def mort(self):
        self._statut = "morte"

    #vie
    @property
    def vie(self):
        return self._vie

    @vie.setter
    def vie(self, x):
        self._vie = x
        if self._vie <= 0:
            self._vie = 0
            self.mort()

    def recoit_degats(self, x):
        self.vie -= x

    #nourriture
    @property
    def nourriture(self):
        return self._nourriture

    @nourriture.setter
    def nourriture(self, quantite: int):
        self._nourriture = quantite
        if self._nourriture > 100:
            self._nourriture = 100
        if self._nourriture <= 0:
            self._nourriture = 0
            self.mort()

    def manger(self, x: int):
        self.nourriture += x
        self.developpement(x/2)

    def developpement(self,x):
        pass

    def se_deplacer(self):
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        choix = []

        pos_actuelle = self._pos_x, self._pos_y
        self.chemin_retour.append(pos_actuelle)
        """vérifier si ça fonctionne"""

        for x,y in directions:
            depla_x, depla_y = self.pos_x + x, self.pos_y + y
            if 0 <= depla_x <= taille and 0 <= depla_y <= taille:
                choix.append([depla_x,depla_y])

        if choix:
            self.pos_x, self.pos_y = random.choices(choix, k=1)[0]


    def trouve_nourriture(self, source):
        #si pos actuelle = pos nourriture => retourner au nid en déposant phéromones sur le chemin
        if self._pos_x == source.pos_x and self._pos_y == source.pos_y:
            if self._nourriture < 80:
                quantite_manger=source.quantite * 0.05
                self.manger(quantite_manger)
            else: quantite_manger=0

            quantite_dispo = source.quantite - quantite_manger
            quantite_a_transporter = min(quantite_dispo, self._capacite_transport - self._transport_nourriture)
            self._transport_nourriture += quantite_a_transporter

            source.perd_nourriture(quantite_manger + quantite_a_transporter) #retire a la source la quantité prise

            self.mode_retour=True
            self._chemin_retour.append((self._pos_x, self._pos_y))
            pass

    def trouve_danger(self):
        #déposer phéromones en retournant au nid ?
        pass

    #définis si fourmi retourne au nid ou non
    @property
    def mode_retour(self):
        return self._mode_retour

    @mode_retour.setter
    def mode_retour(self, bool):
        self._mode_retour = bool

    #définit le chemin de retour au nid
    @property
    def chemin_retour(self):
        return self._chemin_retour

    @chemin_retour.setter
    def chemin_retour(self, nouveau_chemin):
        self._chemin_retour = nouveau_chemin

    def retourner_au_nid(self):
        if self._mode_retour:
            if self._chemin_retour:
                pos_precedente = self._chemin_retour.pop()
                self.pos_x, self.pos_y = pos_precedente
                case_phero = grille_phero[self.pos_y][self.pos_x]
                if self._transport_nourriture > 0:
                    case_phero.deposer_pheromones("nourriture", self._transport_nourriture / 10)
                self.retourner_au_nid()
            else:
                nid.ajouter_nourriture(self._transport_nourriture)
                self._transport_nourriture = 0
                self.mode_retour = False

#differentes pheromones et la quantitée
class Pheromones:
    def __init__(self):
        self._type_pheromones = {
            "nourritures":0.0,
            "danger":0.0,
            "nid":0.0,
        }

    def deposer_pheromones(self,type_pheromones,quantite):
        self._type_pheromones[type_pheromones] += quantite



class Reine(Fourmis):
    def __init__(self, vie,statut,pheromones, pos_x, pos_y,nourriture,mode_retour=False,chemin_retour:list=[],couleur="#F5CC00"):
        super().__init__(chemin_retour=chemin_retour,pheromones=pheromones,pos_x=pos_x, pos_y=pos_y,
                         statut=statut,vie=vie,nourriture=nourriture,mode_retour=mode_retour)
        self._couleur = couleur

    def ponte(self):
        global nbr_fourmis
        nbr_fourmis += 1

        colonie[nbr_fourmis] = Larve()
        """mettre pos actuelle comme propriété pour larve ?"""


class Ouvriere(Fourmis):
    def __init__(self, vie, pos_x,pos_y, pheromones, statut, nourriture,mode_retour=False,chemin_retour:list=[],couleur="#000000"):
        super().__init__(chemin_retour=chemin_retour,pheromones=pheromones,pos_x=pos_x, pos_y=pos_y,
                         statut=statut,vie=vie,nourriture=nourriture,mode_retour=mode_retour)
        self._couleur = couleur

    def construction_nid(self):
        pass

    def explore(self):
        pass

    def construit_nid(self):
        pass
        #dépose phéromones nidification ?


class Soldat(Fourmis):
    def __init__(self,
                 pos_x,
                 pos_y,
                 mode_retour=False,
                 chemin_retour:list=[],
                 pheromones:str="",
                 statut:str="vivante",
                 vie:int=100,
                 nourriture:int=100,
                 attaque:int=20,
                 couleur="#FF6F00"
                 ):
        super().__init__(chemin_retour=chemin_retour,pheromones=pheromones,pos_x=pos_x, pos_y=pos_y,
                         statut=statut,vie=vie,nourriture=nourriture,mode_retour=mode_retour)
        self._attaque = attaque
        self._couleur = couleur

    #attaque et augmentation de l'attaque (croissance)
    @property
    def attaque(self):
        return self._attaque

    @attaque.setter
    def attaque(self,x):
        self._attaque += x
        if self._attaque >= 100:
            self._attaque = 100

    def croissance(self,x):
        self.attaque += x
        """Mettre timer pour que tous les x temps l'attaque augmente"""

    def attaquer(self, cible):
        cible.recoit_degats(self._attaque)


class Larve(Fourmis):
    def __init__(
        self,
        pos_x,
        pos_y,
        mode_retour=False,
        chemin_retour: list = [],
        vie:int=30,
        pheromones=None,
        nourriture:int=100,
        statut:str="vivante",
        croissance:int=0,
        couleur="#FF98EB"
    ):
        super().__init__(chemin_retour=chemin_retour,pheromones=pheromones,pos_x=pos_x, pos_y=pos_y,
                         statut=statut,vie=vie,nourriture=nourriture,mode_retour=mode_retour)
        self._croissance = croissance
        self._couleur = couleur

    @property
    def croissance(self):
        return self._croissance

    @croissance.setter
    def croissance(self,x):
        self._croissance = x
        if self._croissance >= 100:
            self._croissance = 100
            self.eclore()

    def developpement(self,x):
        self.croissance += x

    def eclore(self):
        global nbr_fourmis
        nbr_fourmis += 1

        options=["Reine", "Soldat", "Ouvriere"]
        chances=[1,9.5,89.5] #pourcentages de chances de chaque type de fourmis

        #choix au hasard nouvelle fourmis
        nouvelle_fourmis = random.choices(options, weights=chances, k=1)[0]

        #création nouvelle fourmis
        if nouvelle_fourmis == "Ouvriere":
            colonie[nbr_fourmis] = Ouvriere()
        elif nouvelle_fourmis == "Soldat":
            colonie[nbr_fourmis] = Soldat()
        else:
            colonie[nbr_fourmis] = Reine()

        """supprimer cette instance pour faire moins
         1 larve vu qu'elle vient d'éclore ?"""


#class sources nourriture
class SourceNourriture:
    def __init__(self, pos_x:int, pos_y:int, statut:str="plein",quantite:int=250, couleur="#00FF4D"):
        self._quantite = quantite
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._statut = statut
        self._couleur = couleur

    #définit quantite de nourriture restante
    @property
    def quantite(self):
        return self._quantite

    @quantite.setter
    def quantite(self,x):
        self._quantite = x

    #diminue quantite de nourriture restante quand fourmis
    #viennent en chercher
    def perd_nourriture(self,x):
        self.quantite -= x
        if self._quantite <= 0:
            self._quantite = 0
            self.statut = "vide"

    #définit si source est vide ou non
    @property
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self,x):
        self._statut = x

    #définit position de la source
    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self,x):
        self._pos_x = x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, y):
        self._pos_y = y


    def dissparaitre(self):
        pass
        #si source vide, faire disparaitre de la carte ?

    """générer source de temps en temps dans un autre fichier ?"""
