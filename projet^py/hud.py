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


fenetre.mainloop()
