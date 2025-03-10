##############################################
#  PARTIE 2 - étude des graphes non valués   #
##############################################

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Charger les données
def charger_donnees():
    essain_low_DF = pd.read_csv("topology_low.csv")
    essain_avg_DF = pd.read_csv("topology_avg.csv")
    essain_high_DF = pd.read_csv("topology_high.csv")
    return [essain_low_DF, essain_avg_DF, essain_high_DF]

# Créer un graphe
def creer_graphe(essain_DF, portee):
    G = nx.Graph()
    positions = {row['sat_id']: (row['x'], row['y'], row['z']) for idx, row in essain_DF.iterrows()}
    for i in positions:
        for j in positions:
            if i != j:
                dist = np.linalg.norm(np.array(positions[i]) - np.array(positions[j]))
                if dist <= portee:
                    G.add_edge(i, j)
    return G

# Analyser les caractéristiques du graphe
def analyser_graphe(G):
    resultats = {}
    
    # Degré
    degrees = np.array([deg for n, deg in G.degree()])
    resultats['Distribution des Degrés'] = np.bincount(degrees)
    
    # Coefficient de clustering
    coeffs_clustering = nx.clustering(G)
    resultats['Distribution de Clustering'] = list(coeffs_clustering.values())
    
    # Composantes connexes
    composantes = list(nx.connected_components(G))
    resultats['Nombre de Composantes Connexes'] = len(composantes)
    resultats['Tailles des Composantes Connexes'] = [len(c) for c in composantes]
    
    # Cliques
    cliques = list(nx.find_cliques(G))
    resultats['Nombre de Cliques'] = len(cliques)
    resultats['Tailles des Cliques'] = [len(c) for c in cliques]
    
    # Distribution des plus courts chemins (en nombre de sauts)
    plus_court_chemins = []
    # Pour chaque composante connexe
    for comp in nx.connected_components(G):
        subG = G.subgraph(comp)
        sp_lengths = dict(nx.shortest_path_length(subG))
        for src, dist_dict in sp_lengths.items():
            for dst, dist in dist_dict.items():
                #  src < dst pour éviter les doublons(comme (u, v) et (v, u))
                if src < dst:
                    plus_court_chemins.append(dist)
    
    resultats['Distribution des Plus Courts Chemins'] = plus_court_chemins

    return resultats


#sharex=True pour partager la même échelle sur l'axe x
dataframes = charger_donnees()
portees = [20000, 40000, 60000]
labels_densites = ['faible', 'moyenne', 'forte']

fig_degrees, axes_degrees = plt.subplots(nrows=3, ncols=3, figsize=(15, 15),sharex=True)
fig_degrees.subplots_adjust(hspace=0.5, wspace=0.3)
fig_degrees.suptitle("Distribution du degré", fontsize=16)

fig_clustering, axes_clustering = plt.subplots(nrows=3, ncols=3, figsize=(15, 15),sharex=True)
fig_clustering.subplots_adjust(hspace=0.5, wspace=0.3)
fig_clustering.suptitle("Distribution du coefficient de clustering", fontsize=16)

fig_composantes, axes_composantes = plt.subplots(nrows=3, ncols=3, figsize=(15, 15), sharex=True)
fig_composantes.subplots_adjust(hspace=0.5, wspace=0.3)
fig_composantes.suptitle("Nombre de composantes connexes (et leurs ordres)", fontsize=16)

fig_cliques, axes_cliques = plt.subplots(nrows=3, ncols=3, figsize=(15, 15), sharex=True)
fig_cliques.subplots_adjust(hspace=0.5, wspace=0.3)
fig_cliques.suptitle("Distribution des cliques", fontsize=16)


fig_plus_court_chemins, axes_plus_court_chemins = plt.subplots(nrows=3, ncols=3, figsize=(15, 15),sharex=True)
fig_plus_court_chemins.subplots_adjust(hspace=0.5, wspace=0.3)
fig_plus_court_chemins.suptitle("Distribution des plus courts chemins", fontsize=16)

for i, df in enumerate(dataframes):
    for j, portee in enumerate(portees):
        G = creer_graphe(df, portee)
        resultats = analyser_graphe(G)
        
        # Distribution du degré
        ax_deg = axes_degrees[i, j]
        ax_deg.bar(range(len(resultats['Distribution des Degrés'])), resultats['Distribution des Degrés'])
        ax_deg.set_title(f'degré - {labels_densites[i]} {portee}m')
        ax_deg.set_xlabel('degré')
        ax_deg.set_ylabel('Nombre')
        
        # Distribution du degré de clustering
        ax_clust = axes_clustering[i, j]
        if len(resultats['Distribution de Clustering']) > 0:
            ax_clust.hist(resultats['Distribution de Clustering'], bins=10, color='red', edgecolor='black')
            ax_clust.set_title(f'Clustering - {labels_densites[i]} {portee}m')
            ax_clust.set_xlabel('Clustering Coefficient')
            ax_clust.set_ylabel('Nombre')
        else:#
            ax_clust.text(0.5, 0.5, 'pas de donnée', horizontalalignment='center', verticalalignment='center')
            ax_clust.set_title(f'Clustering - {labels_densites[i]} {portee}m')
            
        # Nombre de composantes connexes (et leurs ordres)
        ax_comp = axes_composantes[i, j]
        tailles_composantes = resultats['Tailles des Composantes Connexes']

        # Obtenir les fréquences de chaque taille
        unique_sizes, counts = np.unique(tailles_composantes, return_counts=True)

        # Utiliser les tailles uniques comme x et leurs fréquences comme y
        ax_comp.bar(unique_sizes, counts)
        ax_comp.set_title(f'composantes - {labels_densites[i]} {portee}m')
        ax_comp.set_xlabel('Ordre') 
        ax_comp.set_ylabel('Nombre')  

        
        
        # Nombre de cliques (et leurs ordres)
        ax_cliq = axes_cliques[i, j]
        tailles_cliques = resultats['Tailles des Cliques']

        # Obtenir les fréquences de chaque taille de clique
        unique_clique_sizes, clique_counts = np.unique(tailles_cliques, return_counts=True)

        # Utiliser les tailles uniques comme x et leurs fréquences comme y
        ax_cliq.bar(unique_clique_sizes, clique_counts)
        ax_cliq.set_title(f'Cliques - {labels_densites[i]} {portee}m')
        ax_cliq.set_xlabel('Ordre')  
        ax_cliq.set_ylabel('Nombre')  

        
        # Distribution des plus courts chemins
        ax_sp = axes_plus_court_chemins[i, j]
        shortest_path_list = resultats['Distribution des Plus Courts Chemins']
        if len(shortest_path_list) > 0:
            ax_sp.hist(shortest_path_list, bins=range(1, max(shortest_path_list) + 2),
                color='purple', edgecolor='black', align='left')
            ax_sp.set_title(f'Plus courts chemins - {labels_densites[i]} {portee}m')
            ax_sp.set_xlabel('Longeur du chemin')
            ax_sp.set_ylabel('Nombre')
        else:
            ax_sp.text(0.5, 0.5, 'Aucune donnée', horizontalalignment='center', verticalalignment='center')
            ax_sp.set_title(f'Plus courts chemins - {labels_densites[i]} {portee}m')

plt.show()

