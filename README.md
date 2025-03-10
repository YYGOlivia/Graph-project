# Graph Project  

## **Contexte**  
Un essaim de nanosatellites sera déployé en orbite autour de la Lune pour une application d’interférométrie. La communication entre ces satellites repose sur un **routage opportuniste**, où les échanges de données se font uniquement lorsque deux satellites sont à portée l’un de l’autre.  

Les protocoles existants cherchent à **optimiser le taux de livraison des paquets** tout en **réduisant la latence**. Une étude des dynamiques de cet essaim a été menée dans [1] au cours d’une révolution lunaire.  

## **Objectif du projet**  
Analyser les caractéristiques de l’essaim dans trois configurations de densité (faible, moyenne et forte) en représentant et en étudiant ses **propriétés sous forme de graphes**.  

## **Données disponibles**  
Les données de mobilité de l’essaim sont fournies sur Moodle et contiennent les positions \((x, y, z)\) de **100 nanosatellites** :  
- **Densité faible** : `topology_low.csv`  
- **Densité moyenne** : `topology_avg.csv`  
- **Densité forte** : `topology_high.csv`  

Les nanosatellites peuvent **ajuster leur portée de communication** entre **20 km, 40 km et 60 km**, et chaque satellite doit transmettre ses données à tous les autres membres de l’essaim.  

## **Méthodologie**  
Le projet est divisé en trois parties :  

### **1. Modélisation sous forme de graphe**  
Représentation graphique de l’essaim pour :  
- Les trois niveaux de densité (**faible, moyenne, forte**)  
- Les trois portées de transmission (**20 km, 40 km, 60 km**)  

### **2. Étude des graphes non valués**  
Analyse des caractéristiques structurelles pour les **9 configurations possibles** :  
- **Degré moyen et distribution du degré**  
- **Moyenne et distribution du coefficient de clustering**  
- **Nombre et tailles des cliques**  
- **Nombre et tailles des composantes connexes**  
- **Plus courts chemins** : longueur, distribution et nombre de chemins entre les sommets connectés  

### **3. Étude des graphes valués**  
Reprise des analyses précédentes pour une **portée de 60 km**, avec un **coût pondéré des arêtes** défini comme le **carré de la distance** entre deux satellites connectés.  

😊
