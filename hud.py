import tkinter as tk
import fourmis
from Nid_fichier import Nid
import random
from time import sleep

from fourmis import Fourmis

fenetre = tk.Tk()
fenetre.geometry("700x700")          #taimlle fenetre
fenetre.resizable(True, True)

canvas = tk.Canvas(fenetre, width=700, height=700)   #taille de la zone dessinable
canvas.pack()

pos_depart_x, pos_depart_y = 0,0
taille_pixel = 15
taille =700 // taille_pixel #le nombre de case par lignes

#canvas.create_rectangle(pos_depart_x, pos_depart_y, taille_pixel, taille_pixel, fill=couleur_pixel, outline=bordure) # structure d'un pixel


grille_phero = []
for y in range(taille):
    lignes = []
    for x in range(taille):
        lignes.append(fourmis.Pheromones())
    grille_phero.append(lignes)

nbr_source_nourriture = 5 #choix du nombre de source qui appariassent sur la carte
source=[]
nid_noir = Nid(0,0)

THE_GOAT_OF_FOURMIES = Fourmis()

canvas.create_rectangle(nid_noir.pos_x, nid_noir.pos_y, nid_noir.taille, nid_noir.taille, fill=nid_noir.couleur, outline=nid_noir.couleur)

for _ in range(nbr_source_nourriture):
    while True:
        x = random.randint(0,taille-1)
        y = random.randint(0,taille-1)
        if (x,y) != (pos_depart_x,pos_depart_y) and (x,y) != (nid_noir.pos_x,nid_noir.pos_y):
            break
    s=fourmis.SourceNourriture(pos_x=x,pos_y=y)
    source.append(s)
for s in source:
    canvas.create_rectangle(
        s.pos_x*taille_pixel,
        s.pos_y*taille_pixel,
        (s.pos_x+1)*taille_pixel,
        (s.pos_y+1)*taille_pixel,
        fill="#00FF4D",
        outline="white"
    )

fenetre.mainloop()
