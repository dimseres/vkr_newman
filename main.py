import itertools

import matplotlib.pyplot as plt
import networkx as nx
from typing import TypedDict, Dict
from networkx.algorithms.community.centrality import girvan_newman

class GraphDict(TypedDict):
    graph: nx.Graph
    wSet: Dict[str, int]

def create_graph() -> GraphDict:
    graph = {
        "user": [],
        "role": ["organization", "user", "membership"],
        "membership": ["user", "role"],
        "organization": ["user"],
        "course": ["organization"],
        "module": ["course"],
        "unit": ["module", "module"],
        "step": ["unit", "knowledge", "module"],
        "knowledge": ["organization", "course"],
        "task": ["step", "test", "course", "unit"],
        "user_progress": ["course", "user", "step", "task"],
        "test": ["task"],
        # "db": []
        # "amqp": ["organization", "course", "test", "user"],
    }

    graph = {
        "user": [],
        "role": ["organization", "user", "membership"],
        "membership": ["user", "role"],
        "organization": ["user"],

        "course_organization": ["organization"],
        "course": ["course_organization"],
        "module": ["course"],
        "unit": ["module", "module"],
        "step": ["unit", "knowledge", "module"],
        "knowledge": ["course_organization", "course"],
        "task": ["step", "test", "course", "unit"],
        "user_progress": ["course", "user", "step", "task", "course_organization"],
        "test": ["task"],
        # "db": []
        # "amqp": ["organization", "course", "test", "user"],
    }

    # for _, val in graph.items():
    #     val.append("db")

    w_set = {key: 0 for key in graph.keys()}
    all_members = set(graph.keys())

    G = nx.Graph()
    G.add_nodes_from(all_members)

    for edge, vertice in graph.items():
        for col in vertice:
            w_set[col] += 1
            G.add_edge(edge, col, weight=w_set[col])
            # for col, entry in enumerate(thisrow):
            #     if entry >= 1:
            # print(vertice)
    # print(G)
    return {'graph': G, 'wSet': w_set}




created = create_graph()
graph = created['graph']
weight = created['wSet']

# graph = nx.karate_club_graph()
comp = girvan_newman(graph)

node_groups = []
k = 2

idx = 0
for communities in itertools.islice(comp, k):
    if idx > 0:
        for c in communities:
            node_groups.append(list(c))
            print(tuple(sorted(c)))
    idx += 1
# for com in next(communities):


print(node_groups)

color_map = []

# nodes_counts = {key: 0 for x in graph.nodes}

for node in graph:
    if node in node_groups[0]:
        color_map.append("red")
    elif node in node_groups[1]:
        color_map.append("orange")
    elif node in node_groups[2]:
        color_map.append("green")
    elif node in node_groups[3]:
        color_map.append("yellow")
    else:
        color_map.append("blue")

    # nodes_counts[node] = node

totalEdges = len(graph.edges)
sums = []


# подсчитать количество ребер внутри кластера
# подсчитать количество внешних ребер
# собрать в группы
external_links = {key: 0 for key in range(len(node_groups))}
inner_links = {key: 0 for key in range(len(node_groups))}
for idx, cluster_nodes in enumerate(node_groups):
    lookup = [x for x in range(len(node_groups)) if x != idx]
    for cluster_node in cluster_nodes:
        for external_idx in lookup:
            for external_node in node_groups[external_idx]:
                if graph.has_edge(cluster_node, external_node):
                    external_links[idx] += 1
                    print(cluster_node)
            print('----------')



        unique_edges = set()
        inner_links[idx] += len(graph.edges(cluster_node))
    G = nx.Graph()
    G.add_nodes_from(set(cluster_nodes))
    for node in cluster_nodes:
        for inner_node in cluster_nodes:
            if graph.has_edge(node, inner_node):
                G.add_edge(node, inner_node)
    inner_links[idx] = G.edges.__len__()

def calculate_modularity_sum(ls, ms, m):
    return ms - (2 * ms + ls) ** 2 / (4 * m)


for key, edges in external_links.items():
    # clusterEdges = 0
    # for cEdge in node_groups:
    sums.append(calculate_modularity_sum(inner_links[key], edges, totalEdges))

total = (1 / totalEdges) * sum(sums)
print(total)

nx.draw(graph, node_color=color_map, with_labels=True)
plt.show()
