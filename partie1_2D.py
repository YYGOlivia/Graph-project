import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Lecture des fichiers CSV
essain_low_DF = pd.read_csv("topology_low.csv")
essain_avg_DF = pd.read_csv("topology_avg.csv")
essain_high_DF = pd.read_csv("topology_high.csv")


# Portées nominales pour les calculs d'arêtes
portees_nominales = [20000, 40000, 60000]

#######################################################
#  PARTIE 0 - Modélisation du graphe sans les arêtes  #
#######################################################

# Cette fonction permet de créer un graphe à partir d'un DataFrame contenant les informations des satellites.
def creation_graphe_essain(essain_DF):
    # On crée tout d'abord un graphe vide
    essain_Graphe = nx.Graph()

    # Puis on récupère la liste des numéros de sommets
    nums_sat = essain_DF["sat_id"].tolist()

    # On récupère les coordonnées des satellites sous forme de numpy array
    coordonnees_sat = np.array(essain_DF[["x", "y", "z"]])


    for i in range(len(nums_sat)):
        # On ajoute les noeuds (sommets) du graphe
        essain_Graphe.add_node(nums_sat[i], pos=coordonnees_sat[i])

    # On extraie les positions des nœuds
    pos = nx.get_node_attributes(essain_Graphe, 'pos')

    return essain_Graphe, pos, coordonnees_sat, nums_sat


# On crée les graphes des trois essains
essain_graphe_low, pos_low, coordonnees_sat_low, nums_sat_low = creation_graphe_essain(essain_low_DF)
essain_graphe_avg, pos_avg, coordonnees_sat_avg, nums_sat_avg = creation_graphe_essain(essain_avg_DF)
essain_graphe_high, pos_high, coordonnees_sat_high, nums_sat_high = creation_graphe_essain(essain_high_DF)


#######################################################
#  PARTIE 1 - Modélisation du graphe avec les arêtes #
#######################################################

# Cette fonction permet d'ajouter les arêtes entre les satellites si la distance est inférieure à la portée
def ajout_des_aretes(graphe, portee, nums_sat, coordonnees_sat):
    n = len(nums_sat)

    for i in range(n):
        for j in range(i + 1, n):
            coordonnees_sat_i = coordonnees_sat[i]
            coordonnees_sat_j = coordonnees_sat[j]
            distance = np.linalg.norm(coordonnees_sat_i - coordonnees_sat_j)

            # Si la distance est inférieure ou égale à la portée de communication, on ajoute une arête
            if distance <= portee:
                graphe.add_edge(nums_sat[i], nums_sat[j])

    return graphe


# Fonction qui permet d'afficher un graphe en 2D avec arêtes
def affichage_graphe_2D_aretes(graphe, pos, nom_figure):
    # On crée une figure 2D
    fig, ax = plt.subplots()

    # On dessine les nœuds
    for node, (x, y, z) in pos.items():
        ax.scatter(x, y, s=50, label=f'Nœud {node}')
        ax.text(x, y, f'{node}', size=10, zorder=1)

    # Idem pour lesarêtes
    for edge in graphe.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        ax.plot(x, y, 'gray')

    # Configuration du graphe
    ax.set_title(nom_figure)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Cette fonction nous permet d'afficher les graphes en 2D sur une même ligne.
def affichage_graphe_2D_aretes_horizontaux(essain_graphe, pos, coordonnees_sat, nums_sat, portees, densite):
    # On crée une figure avec 3 sous-graphes
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Graphe de densité {densite} pour différentes portées", fontsize=16)
    
    for ax, portee in zip(axes, portees):
        # On ajoute les arêtes en fonction de la portée
        graphe_temp = ajout_des_aretes(essain_graphe.copy(), portee, nums_sat, coordonnees_sat)

        # On dessine les nœuds
        for node, (x, y, z) in pos.items():
            ax.scatter(x, y, s=50, label=f'Nœud {node}')
            ax.text(x, y, f'{node}', size=8, zorder=1)

        # Puis les arêtes
        for edge in graphe_temp.edges():
            x = [pos[edge[0]][0], pos[edge[1]][0]]
            y = [pos[edge[0]][1], pos[edge[1]][1]]
            ax.plot(x, y, 'gray')

        # Configuration
        ax.set_title(f"Portée : {portee} m")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        ax.axis('equal')

    plt.tight_layout()
    plt.show()

# Appels pour les différentes densités :
affichage_graphe_2D_aretes_horizontaux(essain_graphe_low, pos_low, coordonnees_sat_low, nums_sat_low, portees_nominales, "faible")
affichage_graphe_2D_aretes_horizontaux(essain_graphe_avg, pos_avg, coordonnees_sat_avg, nums_sat_avg, portees_nominales, "moyenne")
affichage_graphe_2D_aretes_horizontaux(essain_graphe_high, pos_high, coordonnees_sat_high, nums_sat_high, portees_nominales, "forte")