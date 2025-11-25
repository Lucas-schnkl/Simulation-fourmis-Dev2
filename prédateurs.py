class Predateur:
    def __init__(self, pos_x:int = 0, pos_y:int = 0, faim=True, couleur="#FF0000",vie=200,attaque=10, nb_a_manger = 1, statut:bool = True):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self._faim = faim      # après combat faire dans une fct a part que sa faim True // faim = false le fera partir de la map
        self._couleur = couleur
        self._vie = vie
        self._attaque = attaque
        self._nb_a_manger = nb_a_manger  #nb de fourmis qu'il doit manger pour que faim passe à false
        self._statut = statut
    
    def chasser(self):
        pass

    @property
    def vie(self):
        return self._vie

    @vie.setter
    def vie(self,vie):
        self._vie = vie
        if self._vie <= 0 :
            self._vie = 0
            self._statut = False

    @property
    def nb_a_manger(self):
        return self._nb_a_manger

    @nb_a_manger.setter
    def nb_a_manger(self,nb_a_manger):
        self._nb_a_manger = nb_a_manger
        if self._nb_a_manger <= 0 :
            self._faim = False

class Arnaud(Predateur):
    def __init__(self, pos_x:int = 0, pos_y:int = 0, faim=True, couleur="#FF0000",vie=5,attaque=2, nb_a_manger = 15000):
        super().__init__(pos_x,pos_y,faim,couleur,vie,attaque,nb_a_manger)




