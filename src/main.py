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
#                               Fonctions de routage                                           #
################################################################################################
def routage_statique(G, source, dest):
    return nx.shortest_path(G,source,dest)

def routage_partCharge(G,source,dest):
    cheminMax = 0
    cheminDuMax = None
    for path in nx.all_simple_paths(G,source,dest):
        capaChemin = capa_chemin = sum(G[u][v].get('capacity', float('inf')) for u, v in zip(path[:-1], path[1:]))
 
        if  capaChemin > cheminMax:
            cheminMax = capaChemin
            cheminDuMax = path
    return cheminDuMax

################################################################################################
#                                       Fonctions                                              #
################################################################################################

# Fonction de routage statique
def appel(env, G, duree,chemin):
    global appels_bloques, total_appels
    total_appels += 1
    
    
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
def simulation (env,G,i,choix):
    compte = 0
    while True:
        compte += 1
        yield env.timeout(2/i)
        source, dest = random.sample(["CA1","CA2","CA3"], 2)
        if choix == 1:
            chemin = routage_statique(G,source,dest)
        elif choix ==2:
            chemin = routage_partCharge(G,source,dest)
        else :
            print("erreur")
        env.process(appel(env, G, random.randint(1, 5),chemin))
    
################################################################################################
#                                       Simulation                                             #
################################################################################################
simu = range(1,1001,20) 
result = []
result1= []
for i in simu:
    env = simpy.Environment()
    total_appels = 0
    appels_bloques = 0
    env.process(simulation(env,G,i,1))
    env.run(until=50)
    result.append(appels_bloques/total_appels)

for i in simu:
    env = simpy.Environment()
    total_appels = 0
    appels_bloques = 0
    env.process(simulation(env,G,i,2))
    env.run(until=50)
    result1.append(appels_bloques/total_appels)


plt.semilogx(simu, result, label="Scénario 1")
plt.semilogx(simu, result1, label="Scénario 2")
plt.grid(True)
plt.legend()
plt.title("Comparaison des scénarios")
plt.xlabel("Simu (paramètre)")
plt.ylabel("Taux d'appels bloqués")

# Affichage
plt.show()
