import networkx as nx
import matplotlib.pyplot as plt
import simpy
import random

#Création de la fonction d'appelle
def appel(env):
    for loop in range (10):
        duree = random.randint(1,5)



# Création des noeuds 
G = nx.Graph()
G.add_node("CTS1")
G.add_node("CTS2")
G.add_node("CA1")
G.add_node("CA2")
G.add_node("CA3")
G.add_node("U1")
G.add_node("U2")
G.add_node("U3")

# Création des arrêtes
G.add_edge("CTS1", "CA1", weight=100)
G.add_edge("CTS1", "CA2", weight=100)
G.add_edge("CTS1", "CA3", weight=100)
G.add_edge("CTS1", "CTS2", weight=1000)
G.add_edge("CTS2", "CA1", weight=100)
G.add_edge("CTS2", "CA2", weight=100)
G.add_edge("CTS2", "CA3", weight=100)
G.add_edge("CA1", "U1")
G.add_edge("CA1", "CA2", weight=10)
G.add_edge("CA2", "U2")
G.add_edge("CA2", "CA3", weight=10)
G.add_edge("CA3", "U3")

# Position des noeuds pour créer le graphe
pos = {
    "CTS1": (1, 1),
    "CTS2": (2, 1),
    "CA1": (1, 0),
    "CA2": (2, 0),
    "CA3": (3, 0),
    "U1": (1, -1),
    "U2": (2, -1),
    "U3": (3, -1),
}

# Affichage du graphe
plt.figure(figsize=(8, 8))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lime", font_size=10, font_weight="bold")
plt.show()