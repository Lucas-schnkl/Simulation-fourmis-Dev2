import json
import random
from fourmis import Fourmis, Reine, Soldat
from environnement import Environnement
from nid import Nid
from source_nourriture import SourceNourriture
from predateur import Predateur
from test_unitaires import NidError


#variable globale
simulation_active = False
mon_canvas = None
env = None
vitesse_simulation = 100 # Variable pour contrôler la vitesse (Défaut: 100ms)


def initialiser_canvas(canvas_recu):
    #Récupère le canvas depuis debut_hud.py
    global mon_canvas
    mon_canvas = canvas_recu

def set_vitesse(nouvelle_vitesse):
    # Change la vitesse de la simulation
    global vitesse_simulation
    vitesse_simulation = nouvelle_vitesse
    print(f"Vitesse réglée à : {nouvelle_vitesse} ms")

def initialiser_simulation():
    #Crée l'environnement, le nid, les fourmis (Code venant de main.py)
    global env
    #1 Création environnement
    env = Environnement(largeur=1200, hauteur=750, taille_pixel=10)

    #2 Création du nid
    nid = Nid(envi=env, pos_x=35, pos_y=35)
    env.ajouter_nid(nid)

    #3 Ajouter la Reine
    env.ajouter_fourmi(Reine(pos_x=nid.pos_x, pos_y=nid.pos_y, pheromones=""))

    #4 Ajouter des fourmis ouvrières
    for _ in range(50):
        env.ajouter_fourmi(Fourmis(pos_x=nid.pos_x, pos_y=nid.pos_y, pheromones=""))

    #5 Ajouter des soldats
    for _ in range(5):
        #spawn autour du nid
        env.ajouter_fourmi(Soldat(pos_x=nid.pos_x + random.randint(-2, 2),
                                  pos_y=nid.pos_y + random.randint(-2, 2)))

    #6 Ajouter des sources de nourriture
    env.generer_sources()

    #7 Ajouter un prédateur
    for _ in range(3):  # Changez 3 par le nombre voulu
        xp = random.randint(10, 100)  # Position aléatoire pour éviter qu'ils soient tous au même endroit
        yp = random.randint(10, 100)
        env.ajouter_predateur(Predateur(envi=env, pos_x=xp, pos_y=yp))

def start():
    global simulation_active
    #Si la simulation tourne => skip
    if simulation_active:
        return

    print("Démarrage de la simulation")
    simulation_active = True

    # Si envi existe pas encore => crée
    if env is None:
        initialiser_simulation()

    boucle_animation()

def stop():
    global simulation_active
    simulation_active = False
    print("Simulation arrêtée.")

def sauvegarde():
    print("Sauvegarde (pas encore implémenté)")

class ErreurJSON(Exception):
    #Exception pour les erreurs de chargement JSON
    pass

def recharge():
    global mon_canvas
    try:
        with open("canvas.json", "r", encoding="utf-8") as f:
            contenu = json.load(f)

    except FileNotFoundError:
        raise ErreurJSON("Il n'existe aucun fichier de sauvegarde.")
    except json.JSONDecodeError:
        raise ErreurJSON("Fichier de sauvegarde corrompu")

    mon_canvas.delete("all")  # efface le canvas avant de redessiner

    for cont in contenu:
        if cont["type"] == "rectangle":
            mon_canvas.create_rectangle(*cont["coords"], fill=cont["fill"])

        elif cont["type"] == "oval":
            mon_canvas.create_oval(*cont["coords"], fill=cont["fill"])
        elif cont["type"] == "text":
            # Gestion du texte pour apres peut etre
            pass

        else:
            raise ValueError("quelqu'un a rajouter plus que des oval ou des rectangles")


def boucle_animation():
    #met à jour le jeu et redessine tout
    global simulation_active, env, mon_canvas, vitesse_simulation

    if not simulation_active:
        return
        # Mouvements

        # Déplacement toutes fourmis
    for f in env.fourmis:
        f.se_deplacer(env)

        # Déplacement prédateur
    for p in env.predateurs:
        p.se_deplacer(env)
        p.manger(env)

    if env.nid:
        env.nid.cycle_de_vie()

    env.evaporation()
    #Mise à jour graphique
    dessiner_tout()

    #GESTION DE LA VITESSE
    # Utilise la variable vitesse_simulation modifiée par les boutons
    mon_canvas.after(vitesse_simulation, boucle_animation)


def dessiner_tout():
    # Efface et redessine tout l'environnement
    global env, mon_canvas

    mon_canvas.delete("all")

    taille = env.taille_pixel

    # DESSINELE BORD DE LA CARTE (Cadre Noir)
    largeur_pix = env.largeur_grille * taille
    hauteur_pix = env.hauteur_grille * taille
    mon_canvas.create_rectangle(0, 0, largeur_pix, hauteur_pix, outline="black", width=3)

    # Dessine NID (Orange)
    if env.nid:
        x, y = env.nid.pos_x * taille, env.nid.pos_y * taille
        # plus grand que les fourmis
        mon_canvas.create_rectangle(x, y, x + taille, y + taille, fill=env.nid.couleur, outline="")
        # dessine cases étendues du nid
        for cx, cy in env.nid.cases:
            px, py = cx * taille, cy * taille
            mon_canvas.create_rectangle(px, py, px + taille, py + taille, fill="#CC6600", outline="")
    else:
        raise NidError("Le nid n'existe pas")

    # Dessine SOURCES de nourri (Rond Vert)
    # On utilise le générateur pour ne récupérer que les sources actives
    sources_a_dessiner = env.generateur_sources_actives()

    infos_sources = list(map(lambda s: (s._pos_x * taille, s._pos_y * taille, s.compteur), sources_a_dessiner))

    for sx, sy, s_valeur in infos_sources:
        mon_canvas.create_oval(sx, sy, sx + taille, sy + taille, fill="#00FF4D", outline="")
        # Affiche la quantité restante
        mon_canvas.create_text(sx + taille / 2, sy + taille / 2, text=str(s_valeur), font=("Arial", 8))

    # Dessine les PREDA (Rond Rouge)
    for pred in env.predateurs:
        x, y = pred.pos_x * taille, pred.pos_y * taille
        mon_canvas.create_oval(x, y, x + taille, y + taille, fill="red", outline="black", width=2)

    # Dessine FOURMIS (Petits ronds de couleur)
    fourmis_vivantes = list(filter(lambda f: f.vivante, env.fourmis))
    compteur_fourmis = len(fourmis_vivantes)

    for f in fourmis_vivantes:
        x, y = f.pos_x * taille, f.pos_y * taille
        # La Reine est un peu plus grosse
        r = taille if isinstance(f, Reine) else taille
        mon_canvas.create_oval(x, y, x + r, y + r, fill=f.couleur, outline="")

    mon_canvas.create_text(50, 20, text=f"Fourmis: {compteur_fourmis}",font=("Arial", 12, "bold"))  # Affiche nombre total en haut à gauche pour vérif

    try :
        nb_larves = len(env.nid.larves)

        mon_canvas.create_text(50, 40, text=f"Larves: {nb_larves}", font=("Arial", 10), fill="blue")

    except:
        print("Le nid n'existe pas")

