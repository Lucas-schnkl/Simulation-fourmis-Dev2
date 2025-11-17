import tkinter as tk
import fourmies

fenetre = tk.Tk()
fenetre.geometry("700x700")          #taimlle fenetre
fenetre.resizable(True, True)

canvas = tk.Canvas(fenetre, width=700, height=700)   #taille de la zone dessinable
canvas.pack()

pos_depart_x, pos_depart_y = 0,0
taille_pixel = 15
couleur_pixel = "#F5CC00"
bordure = "white"
canvas.create_rectangle(pos_depart_x, pos_depart_y, taille_pixel, taille_pixel, fill=couleur_pixel, outline=bordure) # structure d'un pixel
taille =700 // taille_pixel #le nombre de case par lignes

grille_phero = []
for y in range(taille):
    lignes = []
    for x in range(taille):
        lignes.append(fourmies.Pheromones())
    grille_phero.append(lignes)

nbr_source_nourriture = 5 #choix du nombre de source qui appariassent sur la carte
source=[]
for _ in range(nbr_source_nourriture):
    while True:
        x = random.randint(0,taille-1)
        y = random.randint(0,taille-1)
        if (x,y) != (pos_depart_x,pos_depart_y) and (x,y) != (nid.pos_x,nid.pos_y):
            break
    s=fourmies.SourceNourriture(pos_x=x,pos_y=y)
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
