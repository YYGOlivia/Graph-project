import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance

# On charge les données
def charger_donnees():
    essaim_faible_DF = pd.read_csv("topology_low.csv")
    essaim_moyen_DF = pd.read_csv("topology_avg.csv")
    essaim_fort_DF = pd.read_csv("topology_high.csv")
    return [essaim_faible_DF, essaim_moyen_DF, essaim_fort_DF]

# On crée un graphe
def creer_graphe(essaim_DF, portee):
    graphe = nx.Graph()
    positions = {ligne['sat_id']: (ligne['x'], ligne['y'], ligne['z']) for idx, ligne in essaim_DF.iterrows()}
    for i in positions:
        for j in positions:
            if i != j:
                distance_calculee = np.linalg.norm(np.array(positions[i]) - np.array(positions[j]))
                if distance_calculee <= portee:
                    graphe.add_edge(i, j)
    return graphe

# On analyse les caractéristiques du graphe
def analyser_graphe(graphe):
    resultats = {}
    degres = np.array([degre for n, degre in graphe.degree()])
    resultats['Degré Moyen'] = np.mean(degres) if len(degres) > 0 else 0
    resultats['Distribution des Degrés'] = np.bincount(degres) if len(degres) > 0 else np.array([])

    coefficients_clustering = nx.clustering(graphe)
    resultats['Coefficient de Clustering Moyen'] = np.mean(list(coefficients_clustering.values())) if coefficients_clustering else 0

    composantes_connexes = list(nx.connected_components(graphe))
    resultats['Nombre de Composantes Connexes'] = len(composantes_connexes)
    resultats['Tailles des Composantes Connexes'] = [len(composante) for composante in composantes_connexes]

    cliques = list(nx.find_cliques(graphe))
    resultats['Nombre de Cliques'] = len(cliques)
    resultats['Tailles des Cliques'] = [len(clique) for clique in cliques]

    # On calcule les plus courts chemins pour chaque composante connexe
    plus_courts_chemins = []
    for composante in composantes_connexes:
        sous_graphe = graphe.subgraph(composante)
        longueurs_chemins = dict(nx.shortest_path_length(sous_graphe))
        for src, dist_dict in longueurs_chemins.items():
            for dst, dist in dist_dict.items():
                if src < dst:
                    plus_courts_chemins.append(dist)

    if plus_courts_chemins:
        resultats['Longueur Moyenne des Chemins'] = np.mean(plus_courts_chemins)
        resultats['Nombre des Plus Courts Chemins'] = len(plus_courts_chemins)
    else:
        resultats['Longueur Moyenne des Chemins'] = 'N/A'
        resultats['Nombre des Plus Courts Chemins'] = 0

    return resultats

# On calcule la matrice de distance
def calculer_matrice_distances(donnees):
    positions = donnees[['x', 'y', 'z']].values
    return distance.cdist(positions, positions, 'euclidean')

# On analyse les distances
def analyser_distances(donnees):
    matrice_distances = calculer_matrice_distances(donnees)
    distance_minimale = np.min(matrice_distances[np.triu_indices_from(matrice_distances, k=1)])  # k=1 pour exclure la diagonale
    distance_maximale = np.max(matrice_distances)
    return distance_minimale, distance_maximale


dataframes = charger_donnees()
portees = [20000, 40000, 60000]
etiquettes_densite = ['faible', 'moyenne', 'forte']

matrice_donnees = {}

# On collecte les données pour chaque mesure
mesures = [
    'Degré Moyen', 'Coefficient de Clustering Moyen', 'Nombre de Composantes Connexes',
    'Nombre de Cliques', 'Longueur Moyenne des Chemins', 'Nombre des Plus Courts Chemins'
]

for mesure in mesures:
    matrice_donnees[mesure] = pd.DataFrame(index=etiquettes_densite, columns=portees)

for portee in portees:
    for i, df in enumerate(dataframes):
        graphe = creer_graphe(df, portee)
        resultats = analyser_graphe(graphe)
        for mesure in mesures:
            matrice_donnees[mesure].loc[etiquettes_densite[i], portee] = resultats.get(mesure, 'N/A')

# On affiche les données en format de matrice
for mesure, matrice in matrice_donnees.items():
    print(f"\n{mesure} :")
    print(matrice)

# On analyse les distances
fichiers_donnees = ['topology_low.csv', 'topology_avg.csv', 'topology_high.csv']
densites = ['Faible densité', 'Densité moyenne', 'Haute densité']

for fichier, densite in zip(fichiers_donnees, densites):
    donnees = pd.read_csv(fichier)
    distance_minimale, distance_maximale = analyser_distances(donnees)
    print(f"\nDonnées pour {densite} :")
    print(f"Distance minimale : {distance_minimale} mètres")
    print(f"Distance maximale : {distance_maximale} mètres")


