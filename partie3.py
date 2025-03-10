######################################################
#  PARTIE 3 - étude des graphes valués#
######################################################
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

# Créer un graphe valué (portée de 60 km avec poids = distance^2)
def creer_graphe_pond(essain_DF, portee):
    G = nx.Graph()
    positions = {row['sat_id']: (row['x'], row['y'], row['z']) for idx, row in essain_DF.iterrows()}
    
    for i in positions:
        for j in positions:
            if i != j:
                dist = np.linalg.norm(np.array(positions[i]) - np.array(positions[j]))
                if dist <= portee:
                    G.add_edge(i, j, weight=dist**2)  # Poids = distance^2
    return G

# Analyse des plus courts chemins pondérés
def analyser_chemins_lpc_poids(G):
    chemins_lpc_poids = []
    for comp in nx.connected_components(G):
        subG = G.subgraph(comp)
        sp_lengths = dict(nx.all_pairs_dijkstra_path_length(subG, weight='weight'))
        for src, dist_dict in sp_lengths.items():
            for dst, dist in dist_dict.items():
                if src < dst:
                    chemins_lpc_poids.append(dist)

    return chemins_lpc_poids


dataframes = charger_donnees()
density_labels = ['Faible densité', 'Moyenne densité', 'Forte densité']
portee = 60000  # Étude pour la portée de 60 km

path_distributions = {}

for i, df in enumerate(dataframes):
    G = creer_graphe_pond(df, portee)
    weighted_paths = analyser_chemins_lpc_poids(G)
    path_distributions[density_labels[i]] = weighted_paths

# Création de la figure avec 3 sous-graphiques pour chaque densité
#sharex=True pour partager la même échelle sur l'axe x
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6),sharex=True)
fig.suptitle("Distribution des plus courts chemins pondérés (Portée 60km)", fontsize=16)

for i, (label, paths) in enumerate(path_distributions.items()):
    if paths:
        axes[i].hist(paths, bins=30, color='skyblue', edgecolor='black')
        axes[i].set_title(label)
        axes[i].set_xlabel("Distance pondérée (km²)")
        axes[i].set_ylabel("Fréquence")
    else:
        axes[i].text(0.5, 0.5, 'Aucune donnée', horizontalalignment='center', verticalalignment='center', fontsize=12)
        axes[i].set_title(label)
        axes[i].set_xlabel("Distance pondérée (km²)")
        axes[i].set_ylabel("Fréquence")

plt.tight_layout(rect=[0, 0, 1, 0.96])  
plt.show()
