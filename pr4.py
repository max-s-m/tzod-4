import networkx as nx
import matplotlib.pyplot as plt
import random

N = 100 #к-ть вузлів
M = 2 #к-ть зв'язків вузлів
G = nx.barabasi_albert_graph(N, M) #граф типу багатий стає багатшим

def get_largest_connected(graph):
    if len(graph) == 0: return 0
    return len(max(nx.connected_components(graph), key=len))

def simulate_failure(graph, strategy='random'):
    temp_G = graph.copy()
    nodes = list(temp_G.nodes())
    resilience_data = []
    initial_size = get_largest_connected(temp_G)

    if strategy == 'targeted':
        nodes_to_remove = sorted(temp_G.degree, key=lambda x: x[1], reverse=True)
        nodes_to_remove = [n[0] for n in nodes_to_remove]
    else:
        nodes_to_remove = nodes
        random.shuffle(nodes_to_remove)

    for i in range(len(nodes_to_remove)):
        temp_G.remove_node(nodes_to_remove[i])
        size = get_largest_connected(temp_G)
        resilience_data.append(size / initial_size)
    return resilience_data

random_failure = simulate_failure(G, strategy='random')
targeted_attack = simulate_failure(G, strategy='targeted')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
pos = nx.spring_layout(G, seed=42)
node_sizes = [v * 50 for v in dict(G.degree()).values()]
node_colors = [G.degree(n) for n in G.nodes()]

nx.draw_networkx_edges(G, pos, ax=ax1, alpha=0.2, edge_color='gray')
nodes = nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.plasma)
ax1.set_title(f"Graph (N={N})\n(big = importan)", fontsize=14)
ax1.axis('off')

ax2.plot(random_failure, label='Random failures', linewidth=2)
ax2.plot(targeted_attack, label='Targeted failures', linewidth=2, color='red')
ax2.set_xlabel('Destroyed nodes')
ax2.set_ylabel('Largest connected segment')
ax2.set_title('Failure type compare', fontsize=14)
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

print(f"Details:")
print(f"Avg path length: {nx.average_shortest_path_length(G):.2f}")
print(f"Clusterisation: {nx.average_clustering(G):.2f}") #мала - добре
#<50% з'єднано
print(f"Critical collapse (targeted): ~{next(i for i, v in enumerate(targeted_attack) if v < 0.5)} destroyed nodes")