# L'objectif de ce fichier est de représenter dans l'espace (sous forme de graphes),
# les nano-satellites d'un essain. 

# Nous utiliserons pandas pour la gestion des fichiers csv puisque la manipulation de DataFrames est simple.
import pandas as pd

# Nous utiliserons NetworkX pour la modélisation de graphes puisque c'est une bibliothèque populaire et puissante.
import networkx as nx

# Nous utiliserons MatPlotLib pour la représentation spatiale des graphes puisque c'est une bibliothèque avec laquelle nous sommes familiers.
import matplotlib.pyplot as plt

# Ceci nous sert à une représentations 3D des graphes.
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Lecture des fichier csv : chargement dans un DataFrame
essain_low_DF = pd.read_csv("topology_low.csv")
essain_avg_DF = pd.read_csv("topology_avg.csv")
essain_high_DF = pd.read_csv("topology_high.csv")

portees_nominales = [20000, 40000, 60000]

#######################################################
#  PARTIE 0 - Modélisation du graphe sans les arêtes  #
#######################################################

# Cette fonction permet de créer un graphe à partir d'un DataFrame contenant les informations des satellites.
def creation_graphe_essain(essain_DF):

    # Graphe vide
    essain_Graphe = nx.Graph() 

    # On récupère la liste des numéros de sommets
    nums_sat = essain_DF["sat_id"].tolist()

    # On récupère les coordonnées des satellites sous forme de numpy array
    coordonnees_sat = np.array(essain_DF[["x", "y", "z"]])

    for i in range(len(nums_sat)):
        # On ajoute les noeuds (sommets) du graphe
        essain_Graphe.add_node(nums_sat[i], pos=coordonnees_sat[i])

    # On extraie les positions des nœuds
    pos = nx.get_node_attributes(essain_Graphe, 'pos')

    return essain_Graphe, pos, coordonnees_sat, nums_sat


# Création des graphes pour les trois essains
essain_graphe_low,pos_low,coordonnees_sat_low, nums_sat_low = creation_graphe_essain(essain_low_DF)
essain_graphe_avg,pos_avg,coordonnees_sat_avg, nums_sat_avg = creation_graphe_essain(essain_avg_DF)
essain_graphe_high,pos_high,coordonnees_sat_high, nums_sat_high = creation_graphe_essain(essain_high_DF)

    
def affichage_graphe_3D(pos, nom_figure):
    # On crée une figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Puis on dessine les nœuds et ajoutons les labels
    for node, (x, y, z) in pos.items():
        ax.scatter(x, y, z, s=50, label=f'Nœud {node}')
        ax.text(x, y, z, f'{node}', size=10, zorder=1)

    # Enfin, on affiche le graphe avec son nom.
    plt.title(nom_figure)
    plt.show()
    plt.close(fig)

# Affichage des graphes 3D
affichage_graphe_3D(pos_low,"Graphe de l'essain low sans arêtes")
affichage_graphe_3D(pos_avg,"Graphe de l'essain avg sans arêtes")
affichage_graphe_3D(pos_high,"Graphe de l'essain high sans arêtes")

######################################################
#  PARTIE 1 - Modélisation du graphe avec les arêtes #
######################################################

# L'objectif de cette fonction est de calculer pour chaque paire de sommets leur distance et ajouter
# une arête entre eux si leur distance est inférieure à la portée nominale.

# Cette fonction permet d'ajouter les arêtes entre les satellites si la distance est inférieure à la portée
def ajout_des_aretes(graphe, portee, nums_sat, coordonnees_sat):
    n = len(nums_sat)
    min_distance = float('inf')  
    max_distance = 0  

    for i in range(n):
        for j in range(i + 1, n):
            coordonnees_sat_i = coordonnees_sat[i]
            coordonnees_sat_j = coordonnees_sat[j]
            distance = np.linalg.norm(coordonnees_sat_i - coordonnees_sat_j)

            # MàJ des distances minimales et maximales entre les noeuds
            if distance < min_distance:
                min_distance = distance
            if distance > max_distance:
                max_distance = distance
            # Si la distance est inférieure ou égale à la portée de communication, ajoutez un bord
            if distance <= portee:
                graphe.add_edge(nums_sat[i], nums_sat[j])
                                
    return graphe


# Fonction pour afficher les graphes avec les arêtes
def affichage_graphe_3D_aretes(graphe, pos, nom_figure):
    # Créer une figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Dessiner les nœuds et ajouter les labels
    for node, (x, y, z) in pos.items():
        ax.scatter(x, y, z, s=50, label=f'Nœud {node}')
        ax.text(x, y, z, f'{node}', size=10, zorder=1)

    # Dessiner les arêtes
    for edge in graphe.edges():
        x = [pos[edge[0]][0], pos[edge[1]][0]]
        y = [pos[edge[0]][1], pos[edge[1]][1]]
        z = [pos[edge[0]][2], pos[edge[1]][2]]
        ax.plot(x, y, z, 'gray')

    # Enfin, on affiche le graphe avec son nom.
    plt.title(nom_figure)
    plt.show()
    plt.close(fig)

# Fonction pour afficher tous les graphes (avec et sans arêtes)
def afficher_graphiques_complets():
    plt.close('all') # Fermer toutes les figures précédentes


    # Affichage des graphes avec arêtes pour chaque portée
    # Pour le densité faible (low)
    for i, portee in enumerate(portees_nominales):
        essain_graphe_temp = ajout_des_aretes(essain_graphe_low.copy(), portee, nums_sat_low, coordonnees_sat_low)
        affichage_graphe_3D_aretes(essain_graphe_temp, pos_low, f"Graphe de densité faible avec arêtes (portée {portee}m)")
        plt.close() 
    # Pour le densité moyen (avg)
    for i, portee in enumerate(portees_nominales):
        essain_graphe_temp = ajout_des_aretes(essain_graphe_avg.copy(), portee, nums_sat_avg, coordonnees_sat_avg)
        affichage_graphe_3D_aretes(essain_graphe_temp, pos_avg, f"Graphe de densité moyenne avec arêtes (portée {portee}m)")
        plt.close()
    # Pour le densité forte (high)
    for i, portee in enumerate(portees_nominales):
        essain_graphe_temp = ajout_des_aretes(essain_graphe_high.copy(), portee, nums_sat_high, coordonnees_sat_high)
        affichage_graphe_3D_aretes(essain_graphe_temp, pos_high, f"Graphe de densité forte avec arêtes (portée {portee}m)")
        plt.close()

# Appel de la fonction pour afficher tous les graphes
afficher_graphiques_complets()