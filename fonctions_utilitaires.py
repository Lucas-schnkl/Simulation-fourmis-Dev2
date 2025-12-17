import json
import random
from fourmis import Fourmis, Reine, Soldat
from environnement import Environnement
from nid import Nid
from source_nourriture import SourceNourriture
from predateur import Predateur


#variable globale
simulation_active = False
mon_canvas = None
env = None


def initialiser_canvas(canvas_recu):
    #Récupère le canvas depuis debut_hud.py
    global mon_canvas
    mon_canvas = canvas_recu

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
    env.ajouter_predateur(Predateur(envi=env, pos_x=60, pos_y=60))

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

    #objets = []
    #for item in canvas.find_all():
     #   objets.append({
      #      "type": canvas.type(item),
       #     "coords": canvas.coords(item),
        #    "fill": {k: v for k, v in canvas.itemconfig(item).items()}       #le type va contenir la forme (faut pas mettre autre chose que des rectangles ou des ovales), coords les coos, fill la couleur
       # })
     # with open("canvas.json", "w", encoding="utf-8") as f:
     #     json.dump(objets, f, indent=4)

def recharge():
    global mon_canvas
    try:
        with open("canvas.json", "r", encoding="utf-8") as f:
            contenu = json.load(f)

    except FileNotFoundError:
        print("Il n'existe aucun fichier de sauvegarde")  # verif si le fichier existe
        return
    except json.JSONDecodeError:
        print("Fichier de sauvegarde corrompu")
        return

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
    global simulation_active, env, mon_canvas

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

        #  Attention évaporation des phéromones (Optionnel : peut être lourd si fait trop souvent)
        #  env.evaporation()        #ils disparaissent trop vite

        #Mise à jour graphique
    dessiner_tout()

    #GESTION DE LA VITESSE
    # 50 ms = Rapide (20 FPS)
    # 100 ms = Normal (10 FPS)
    # 200 ms = Lent (5 FPS)
    mon_canvas.after(100, boucle_animation)


def dessiner_tout():
    #Efface et redessine tout l'environnement
    global env, mon_canvas

    mon_canvas.delete("all")

    taille = env.taille_pixel

    #DESSINELE BORD DE LA CARTE (Cadre Noir)
    largeur_pix = env.largeur_grille * taille
    hauteur_pix = env.hauteur_grille * taille
    mon_canvas.create_rectangle(0, 0, largeur_pix, hauteur_pix, outline="black", width=3)

    #Dessine NID (Orange)
    if env.nid:
        x, y = env.nid.pos_x * taille, env.nid.pos_y * taille
        #plus grand que les fourmis
        mon_canvas.create_rectangle(x, y, x + taille, y + taille, fill=env.nid.couleur, outline="")
        #dessine cases étendues du nid
        for cx, cy in env.nid.cases:
            px, py = cx * taille, cy * taille
            mon_canvas.create_rectangle(px, py, px + taille, py + taille, fill="#CC6600", outline="")

    #Dessine SOURCES de nourri (Rond Vert)
    for source in env.sources:
        x, y = source._pos_x * taille, source._pos_y * taille
        mon_canvas.create_oval(x, y, x + taille, y + taille, fill="#00FF4D", outline="")
        # Affiche la quantité restante
        mon_canvas.create_text(x + taille / 2, y + taille / 2, text=str(source.compteur), font=("Arial", 8))

    #Dessine les PHERO(Carrés très clairs) - Optionnel
    # for y in range(env.taille_grille):
    #     for x in range(env.taille_grille):
    #         if env.grille_phero[y][x]["danger"] > 0:
    #             px, py = x * taille, y * taille
    #             mon_canvas.create_rectangle(px, py, px+taille, py+taille, fill="#FFCCCC", outline="") # Rouge pâle

    #Dessine les PREDA (Rond Rouge)
    for pred in env.predateurs:
        x, y = pred.pos_x * taille, pred.pos_y * taille
        mon_canvas.create_oval(x, y, x + taille, y + taille, fill="red", outline="black", width=2)

    #Dessine FOURMIS (Petits ronds de couleur)
    compteur_fourmis = 0
    for f in env.fourmis:
        if f.vivante:
            compteur_fourmis += 1
            x, y = f.pos_x * taille, f.pos_y * taille
            # La Reine est un peu plus grosse
            r = taille if isinstance(f, Reine) else taille
            mon_canvas.create_oval(x, y, x + r, y + r, fill=f.couleur, outline="")
    mon_canvas.create_text(50, 20, text=f"Fourmis: {compteur_fourmis}", font=("Arial", 12, "bold"))  #Affiche nombre total en haut à gauche pour vérif

