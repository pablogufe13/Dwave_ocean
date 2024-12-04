import networkx as nx
from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import BinaryQuadraticModel

# Paso 1: Crear un grafo simple
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)])

# Paso 2: Construir el modelo QUBO para el problema de Max-Cut
Q = {}
for u, v in G.edges:
    Q[(u, u)] = Q.get((u, u), 0) + 1
    Q[(v, v)] = Q.get((v, v), 0) + 1
    Q[(u, v)] = Q.get((u, v), 0) - 2

# Crear el modelo
bqm = BinaryQuadraticModel.from_qubo(Q)

# Paso 3: Resolver el problema usando un sampler cuántico
sampler = EmbeddingComposite(DWaveSampler())
response = sampler.sample(bqm, num_reads=100)

# Paso 4: Mostrar resultados
print("Mejores soluciones:")
for sample, energy in response.data(['sample', 'energy']):
    print(f"Solución: {sample}, Energía: {energy}")

# Visualizar el grafo y la partición
import matplotlib.pyplot as plt

best_solution = response.first.sample
colors = ['red' if best_solution[node] == 1 else 'blue' for node in G.nodes]

nx.draw(G, with_labels=True, node_color=colors)
plt.show()
