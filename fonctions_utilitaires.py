import json
import fourmis

def start():
    global cours_utilisation
    cours_utilisation = True

    while cours_utilisation:
        """ à completer avec le code qui joue la simulation """

def stop():
    cours_utilisation = False

def sauvegarde():
    objets = []
    for item in canvas.find_all():
        objets.append({
            "type": canvas.type(item),
            "coords": canvas.coords(item),
            "fill": {k: v for k, v in canvas.itemconfig(item).items()}       #le type va contenir la forme (faut pas mettre autre chose que des rectangles ou des ovales), coords les coos, fill la couleur
        })
      with open("canvas.json", "w", encoding="utf-8") as f:
          json.dump(objets, f, indent=4)


def recharge():
  try:
    with open("canvas.json", "r", encoding="utf-8") as f :
      contenu = json.load(f)

  except FileNotFoundError:
    print("Il n'existe aucun fichier de sauvegarde")    #verif si le fichier existe
    return

  for cont in contenu:
    if contenu["type"] == "rectangle":
      canvas.create_rectangle(*cont["coords"], fill=cont["fill"])
    
    elif contenu["type"] == "oval":
      canvas.create_oval(*cont["coords"], fill=cont["fill"])

    else :
      raise ValueError("quelqu'un a rajouter plus que des oval ou des rectangles")
