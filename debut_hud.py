import tkinter as tk
import fonctions_utilitaires as fu


""" Creation de la fenetre  """
fenetre = tk.Tk()
fenetre.title("Simulation de fourmis")

"""  Creation de la zone dessinable  """
canvas = tk.Canvas(fenetre, width=1200, height=750, bg="white")
canvas.pack()

fu.initialiser_canvas(canvas)

"""  Partie consacrée aux bouttons  """
boutton_emplacement = tk.Frame(fenetre)    #creation de l'emplacement
boutton_emplacement.pack(pady=10)          #pady : la taille des l'emplacement dedier aux bouttons

boutton_recharger = tk.Button(boutton_emplacement, text="recharger",command=fu.recharge)
boutton_recharger.pack(side=tk.RIGHT, padx=0)

boutton_sauvegarde = tk.Button(boutton_emplacement, text="sauvegarde",command=fu.sauvegarde)      #creations de chaque bouttons (le premier boutton a etre cree sera le plus a droite psk side RIGHT)
boutton_sauvegarde.pack(side=tk.RIGHT, padx=0)

# Bouton pour vitesse Rapide (50ms)
boutton_vitesse_rapide = tk.Button(boutton_emplacement, text="vitesse x2", command=lambda: fu.set_vitesse(50))
boutton_vitesse_rapide.pack(side=tk.RIGHT, padx=5)

# Nouveau bouton pour remettre la vitesse normale (100ms)
boutton_vitesse_normale = tk.Button(boutton_emplacement, text="vitesse normale", command=lambda: fu.set_vitesse(100))
boutton_vitesse_normale.pack(side=tk.RIGHT, padx=5)

boutton_stop = tk.Button(boutton_emplacement, text="stop",command=fu.stop)
boutton_stop.pack(side=tk.RIGHT, padx=0)

boutton_start = tk.Button(boutton_emplacement, text="start",command=fu.start)
boutton_start.pack(side=tk.RIGHT, padx=0)

fenetre.mainloop()