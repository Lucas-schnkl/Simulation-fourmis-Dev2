import tkinter as tk

class InterfaceGraphique:
    def __init__(self, env, taille_pixel=10):
        self.env = env
        self.taille_pixel = taille_pixel
        self.taille = 700 // taille_pixel

        self.fenetre = tk.Tk()
        self.fenetre.geometry("700x700")
        self.fenetre.title("Simulation Fourmis / Prédateurs")

        self.canvas = tk.Canvas(self.fenetre, width=700, height=700)
        self.canvas.pack()

        self.objects = {}


    def dessiner_static(self):
        # Dessine le décor une seule fois : nid + sources de nourriture

        # Nid
        n = self.env.nid
        nid_id = self.canvas.create_rectangle(
            n.pos_x * self.taille_pixel,
            n.pos_y * self.taille_pixel,
            (n.pos_x + 1) * self.taille_pixel,
            (n.pos_y + 1) * self.taille_pixel,
            fill= self.env.nid.couleur
        )
        self.objects[n] = nid_id

        # Sources
        for s in self.env.sources:
            sid = self.canvas.create_rectangle(
                s.pos_x * self.taille_pixel,
                s.pos_y * self.taille_pixel,
                (s.pos_x + 1) * self.taille_pixel,
                (s.pos_y + 1) * self.taille_pixel,
                fill=s._couleur
            )
            self.objects[s] = sid

    def dessiner_fourmis(self):
        # Ajoute ou met à jour les fourmis sur le canvas
        for f in self.env.fourmis:
            if f not in self.objects:
                fid = self.canvas.create_oval(
                    f.pos_x * self.taille_pixel,
                    f.pos_y * self.taille_pixel,
                    (f.pos_x + 1) * self.taille_pixel,
                    (f.pos_y + 1) * self.taille_pixel,
                    fill=f._couleur
                )
                self.objects[f] = fid

            # met à jour la position
            self.canvas.coords(
                self.objects[f],
                f.pos_x * self.taille_pixel,
                f.pos_y * self.taille_pixel,
                (f.pos_x + 1) * self.taille_pixel,
                (f.pos_y + 1) * self.taille_pixel
            )

    def dessiner_predateurs(self):
        # Ajoute ou met à jour les prédateurs sur le canvas
        for p in self.env.predateurs:
            if p not in self.objects:
                pid = self.canvas.create_oval(
                    p.pos_x * self.taille_pixel,
                    p.pos_y * self.taille_pixel,
                    (p.pos_x + 1) * self.taille_pixel,
                    (p.pos_y + 1) * self.taille_pixel,
                    fill="red"
                )
                self.objects[p] = pid

            # mise à jour
            self.canvas.coords(
                self.objects[p],
                p.pos_x * self.taille_pixel,
                p.pos_y * self.taille_pixel,
                (p.pos_x + 1) * self.taille_pixel,
                (p.pos_y + 1) * self.taille_pixel
            )

    def update(self):
        # Met à jour toutes les êtres vivants
        self.dessiner_fourmis()
        self.dessiner_predateurs()
        self.fenetre.update()
