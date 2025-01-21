import networkx as nx
import matplotlib.pyplot as plt
import simpy
import random

################################################################################################
#                                       variables et graphe                                    # 
################################################################################################

# Création de l'environnement
env = simpy.Environment()

# Création des noeuds 
G = nx.Graph()
G.add_node("CTS1")
G.add_node("CTS2")
G.add_node("CA1")
G.add_node("CA2")
G.add_node("CA3")

# Création des arrêtes
G.add_edge("CTS1", "CA1", capacity=100)
G.add_edge("CTS1", "CA2", capacity=100)
G.add_edge("CTS1", "CA3", capacity=100)
G.add_edge("CTS1", "CTS2", capacity=1000)
G.add_edge("CTS2", "CA1", capacity=100)
G.add_edge("CTS2", "CA2", capacity=100)
G.add_edge("CTS2", "CA3", capacity=100)
G.add_edge("CA1", "CA2", capacity=10)
G.add_edge("CA2", "CA3", capacity=10)

# Ajout des ressources pour les arrêtes
for u, v in G.edges:
    G[u][v]['current_load'] = 0

appels_bloques = 0
total_appels = 0
################################################################################################
#                                       affichage du graphe                                    # 
################################################################################################

# Position des noeuds pour créer le graphe
pos = {
    "CTS1": (1, 1),
    "CTS2": (2, 1),
    "CA1": (1, 0),
    "CA2": (2, 0),
    "CA3": (3, 0),
}

# Affichage du graphe
#plt.figure(figsize=(8, 8))
#nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightgreen", font_size=10, font_weight="bold")
#plt.show()

################################################################################################
#                                       Fonctions                                              #
################################################################################################

# Fonction de routage statique
def appel(env, G, source, dest, duree):
    global appels_bloques, total_appels
    total_appels += 1
    
    chemin = nx.shortest_path(G, source, dest)
    if all(G[u][v]['current_load'] + 1 <= G[u][v].get('capacity', float('inf')) for u, v in zip(chemin[:-1], chemin[1:])):
        for u, v in zip(chemin[:-1], chemin[1:]):
            G[u][v]['current_load'] += 1

        yield env.timeout(duree)

        for u, v in zip(chemin[:-1], chemin[1:]):
            G[u][v]['current_load'] -= 1

       
    else:
        #on récupère ici les appels bloquès pour les compter
        appels_bloques += 1
        


# Fonction de simulation des appels
def simulation (env,G,i):
    compte = 0
    while True:
        compte += 1
        yield env.timeout(2/i)
        source, dest = random.sample(list(G.nodes), 2)

        env.process(appel(env, G, source, dest, random.randint(1, 5)))
    


################################################################################################
#                                       Simulation                                             #
################################################################################################
simu = range(1,1001,20)
result = []
for i in simu:
    env = simpy.Environment()
    total_appels = 0
    appels_bloques = 0
    env.process(simulation(env,G,i))
    env.run(until=50)
    result.append(appels_bloques/total_appels)

plt.semilogx(simu,result)
plt.grid(True)
plt.legend()

# Affichage
plt.show()
