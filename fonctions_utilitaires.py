import json
import random
from fourmis import Fourmis, Reine, Soldat
from environnement import Environnement
from nid import Nid
from source_nourriture import SourceNourriture
from predateur import Predateur
from test_unitaires import NidError

# =============================================================================
# VARIABLES GLOBALES ET CONFIG
# =============================================================================

simulation_active = False
mon_canvas = None
env = None
vitesse_simulation = 100  # Variable pour contrôler la vitesse (Défaut: 100ms)


# =============================================================================
# INITIALISATION
# =============================================================================

def initialiser_canvas(canvas_recu):
    """Récupère le canvas depuis debut_hud.py"""
    global mon_canvas
    mon_canvas = canvas_recu


def set_vitesse(nouvelle_vitesse):
    """Change la vitesse de la simulation"""
    global vitesse_simulation
    vitesse_simulation = nouvelle_vitesse
    print(f"Vitesse réglée à : {nouvelle_vitesse} ms")


def initialiser_simulation():
    """Crée l'environnement, le nid, les fourmis et prédateurs"""
    global env

    # 1. Création environnement
    env = Environnement(largeur=1200, hauteur=750, taille_pixel=10)

    # 2. Création du nid
    nid = Nid(envi=env, pos_x=35, pos_y=35)
    env.ajouter_nid(nid)

    # 3. Ajouter la Reine
    env.ajouter_fourmi(Reine(pos_x=nid.pos_x, pos_y=nid.pos_y, pheromones=""))

    # 4. Ajouter des fourmis ouvrières
    for _ in range(50):
        env.ajouter_fourmi(Fourmis(pos_x=nid.pos_x, pos_y=nid.pos_y, pheromones=""))

    # 5. Ajouter des soldats (spawn autour du nid)
    for _ in range(5):
        env.ajouter_fourmi(Soldat(pos_x=nid.pos_x + random.randint(-2, 2),
                                  pos_y=nid.pos_y + random.randint(-2, 2)))

    # 6. Ajouter des sources de nourriture
    env.generer_sources()

    # 7. Ajouter des prédateurs
    for _ in range(3):
        xp = random.randint(10, 100)
        yp = random.randint(10, 100)
        env.ajouter_predateur(Predateur(envi=env, pos_x=xp, pos_y=yp))


def start():
    """Lance la boucle de simulation"""
    global simulation_active

    if simulation_active:
        return

    print("Démarrage de la simulation")
    simulation_active = True

    # Si l'environnement n'existe pas encore, on le crée
    if env is None:
        initialiser_simulation()

    boucle_animation()


def stop():
    """Arrête la boucle de simulation"""
    global simulation_active
    simulation_active = False
    print("Simulation arrêtée.")


# =============================================================================
# GESTION SAUVEGARDE
# =============================================================================

def sauvegarde():
    print("Sauvegarde (pas encore implémenté)")


class ErreurJSON(Exception):
    # Exception pour les erreurs de chargement JSON
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
            pass
        else:
            raise ValueError("Type d'objet inconnu dans la sauvegarde")


# =============================================================================
# COEUR DU SYSTÈME
# =============================================================================

def extraire_etat_simulation(env):
    """
    Transforme l'objet complexe 'env' en un dictionnaire de données simples (DTO).
    Cette fonction ne connait PAS Tkinter.
    Elle prépare tout ce qui doit être affiché.
    """
    if not env:
        return None

    # Info générale pour les statistiques
    #Calcule ici pour éviter de le faire dans l'affichage
    fourmis_vivantes = [f for f in env.fourmis if f.vivante]

    etat = {
        "config": {
            "largeur_grille": env.largeur_grille,
            "hauteur_grille": env.hauteur_grille,
            "taille_pixel": env.taille_pixel
        },
        "stats": {
            "nb_fourmis": len(fourmis_vivantes),
            "nb_predateurs": len(env.predateurs),
            "nb_larves": len(env.nid.larves) if env.nid else 0,
            "nb_sources": len(env.sources)  # Juste indicatif
        },
        "entites": []  # Liste de tout ce qu'il faut dessiner
    }

    # 1. Extraction du NID
    if env.nid:
        # Le carré central du nid
        etat["entites"].append({
            "type": "nid_centre",
            "x": env.nid.pos_x,
            "y": env.nid.pos_y,
            "couleur": env.nid.couleur
        })
        # Les agrandissements
        for cx, cy in env.nid.cases:
            etat["entites"].append({
                "type": "nid_case",
                "x": cx,
                "y": cy,
                "couleur": "#CC6600"
            })

    # 2. Extraction des SOURCES (Actives uniquement)
    for s in env.generateur_sources_actives():
        etat["entites"].append({
            "type": "source",
            "x": s._pos_x,
            "y": s._pos_y,
            "valeur": s.compteur,
            "couleur": "#00FF4D"
        })

    # 3. Extraction des PRÉDATEURS
    for p in env.predateurs:
        etat["entites"].append({
            "type": "predateur",
            "x": p.pos_x,
            "y": p.pos_y,
            "couleur": "red"
        })

    # 4. Extraction des FOURMIS VIVANTES
    for f in fourmis_vivantes:
        est_reine = isinstance(f, Reine)
        etat["entites"].append({
            "type": "fourmi",
            "x": f.pos_x,
            "y": f.pos_y,
            "couleur": f.couleur,
            "est_reine": est_reine
        })

    return etat


def afficher_vers_console(etat):
    """
    Permet de suivre la simulation même sans interface graphique.
    """
    if not etat:
        return

    #affiche un résumé simple
    print(f"[SIMULATION] Fourmis: {etat['stats']['nb_fourmis']} | Larves: {etat['stats']['nb_larves']}")
    pass


def afficher_vers_gui(etat, canvas):
    """
     Affichage graphique sur Tkinter.
    """
    if not etat or not canvas:
        return

    # Nettoyage complet
    canvas.delete("all")

    taille = etat["config"]["taille_pixel"]

    # 1. DESSINER le Cadre Noir
    largeur_pix = etat["config"]["largeur_grille"] * taille
    hauteur_pix = etat["config"]["hauteur_grille"] * taille
    canvas.create_rectangle(0, 0, largeur_pix, hauteur_pix, outline="black", width=3)

    # 2. DESSINER LES ENTITÉS
    # L'ordre d'ajout
    # on a fait : Nid -> Sources -> Predateurs -> Fourmis

    for entite in etat["entites"]:
        x, y = entite["x"] * taille, entite["y"] * taille

        if entite["type"] == "nid_centre" or entite["type"] == "nid_case":
            canvas.create_rectangle(x, y, x + taille, y + taille, fill=entite["couleur"], outline="")

        elif entite["type"] == "source":
            canvas.create_oval(x, y, x + taille, y + taille, fill=entite["couleur"], outline="")
            # Affiche la quantité restante au centre
            canvas.create_text(x + taille / 2, y + taille / 2, text=str(entite["valeur"]), font=("Arial", 8))

        elif entite["type"] == "predateur":
            canvas.create_oval(x, y, x + taille, y + taille, fill=entite["couleur"], outline="black", width=2)

        elif entite["type"] == "fourmi":
            # Si c'est une reine, on peut ajuster la taille ici si besoin
            r = taille
            canvas.create_oval(x, y, x + r, y + r, fill=entite["couleur"], outline="")

    # 3. DESSINER LE HUD (TEXTE)
    stats = etat["stats"]

    # Compteur Fourmis
    canvas.create_text(50, 20, text=f"Fourmis: {stats['nb_fourmis']}", font=("Arial", 12, "bold"))

    # Compteur Larves
    canvas.create_text(50, 40, text=f"Larves: {stats['nb_larves']}", font=("Arial", 10), fill="blue")


# =============================================================================
# BOUCLE PRINCIPALE D'ANIMATION
# =============================================================================

def boucle_animation():
    """
    Orchestre la simulation :
    1. Mise à jour Logique (Env)
    2. Extraction des données (Pont)
    3. Mise à jour des Vues (Console & GUI)
    """
    global simulation_active, env, mon_canvas, vitesse_simulation

    if not simulation_active:
        return

    # --- 1. LOGIQUE (Mise à jour du modèle) ---

    # Déplacement toutes fourmis
    for f in env.fourmis:
        f.se_deplacer(env)

    # Déplacement prédateurs
    for p in env.predateurs:
        p.se_deplacer(env)
        p.manger(env)

    # Cycle de vie du nid (naissance fourmis)
    if env.nid:
        env.nid.cycle_de_vie()

    # Gestion de l'environnement (évaporation, nettoyage famine)
    env.evaporation()

    # --- 2. EXTRACTION DES DONNÉES (Le Pont) ---
    # On crée un instantané de la situation
    donnees_du_tour = extraire_etat_simulation(env)

    # --- 3. AFFICHAGE (Les Vues) ---
    # On envoie les données aux différents systèmes d'affichage
    afficher_vers_console(donnees_du_tour)
    afficher_vers_gui(donnees_du_tour, mon_canvas)

    # --- 4. PROGRAMMATION DU PROCHAIN TOUR ---
    mon_canvas.after(vitesse_simulation, boucle_animation)