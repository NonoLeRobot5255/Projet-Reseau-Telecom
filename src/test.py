import networkx as nx
import simpy

def charge(env, graph, path, charge_id):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        print(f"Time {env.now}: Charge {charge_id} traveling from {u} to {v}")
        
        # Simuler le temps de déplacement (par exemple, le poids de l'arête)
        travel_time = graph[u][v].get('weight', 1)
        yield env.timeout(travel_time)
        
        # Ajouter un effet, par exemple, mise à jour des charges sur les arêtes
        graph[u][v]['current_load'] += 1
        print(f"Time {env.now}: Charge {charge_id} reached {v}")
        graph[u][v]['current_load'] -= 1

# Initialisation du graphe avec NetworkX
graph = nx.DiGraph()
graph.add_edge('A', 'B', weight=5, current_load=0)
graph.add_edge('B', 'C', weight=3, current_load=0)

# Simulation avec SimPy
env = simpy.Environment()
path = ['A', 'B', 'C']

# Ajouter plusieurs charges
for charge_id in range(3):
    env.process(charge(env, graph, path, charge_id))

# Lancer la simulation
env.run()
