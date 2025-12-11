def resultats(env):
    fourmis = env.fourmis
    predateurs = env.predateurs
    nid = env.nid
    sources = env.sources
    try:
        with open('resultats.txt', 'w') as f:
            f.write(f"Nombre de fourmis : {len(fourmis)}\n")
            f.write(f"Nombre de predateur(s) : {len(predateurs)}\n")
            f.write(f"Nombre de nid(s) : {len(nid)}\n")
            f.write(f"Nombre de sources : {len(sources)}\n")

        print("Fichiers résulats.json crée")
    except:
        print("Erreur avec le fichier de résultats")