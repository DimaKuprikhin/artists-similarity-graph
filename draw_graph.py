import matplotlib.pyplot as plt
import networkx as nx
import json

G = nx.Graph()

with open('result_ovsyankin.json', 'r') as f:
    data = json.loads(f.read())

# edges = {}
# for artist, similar_artists in data.items():
#     for node in similar_artists:
#         from_ = artist
#         to = node['name']
#         if from_ > to:
#             tmp = from_
#             from_ = to
#             to = tmp
#         dist = round((1.0 / float(node['match'])) ** 2, 3)
#         item = f'{from_}\t{to}'
#         if item in edges:
#             edges[item] = edges[item] / 2.0 + dist
#         else:
#             edges[item] = 2.0 * dist

def get_dist(match: float) -> float:
    return 1.0
    if match == 1.0:
        return 1.0
    if match >= 0.9:
        return 1.5
    if match >= 0.8:
        return 2.5
    if match >= 0.6:
        return 4.5
    return 8.0

edges = {}
for artist, similar_artists in data.items():
    for node in similar_artists:
        match = round(float(node['match']), 3)
        dist = get_dist(match)
        from_ = artist
        to = node['name']
        if from_ > to:
            tmp = from_
            from_ = to
            to = tmp
        item = f'{from_}\t{to}'
        if item not in edges:
            edges[item] = dist
        else:
            edges[item] = (edges[item] + dist) / 2.0

for edge, dist in edges.items():
    artists = edge.split('\t')
    assert len(artists) == 2
    G.add_edge(artists[0], artists[1], weight=dist)

esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.8]

pos = nx.spring_layout(G)  # positions for all nodes - seed for reproducibility

# nodes
nx.draw_networkx_nodes(G, pos, node_size=20)

# edges
nx.draw_networkx_edges(
    G, pos, edgelist=esmall, width=0.2, alpha=0.5, edge_color="b",
)

# node labels
nx.draw_networkx_labels(G, pos, font_size=1, font_family="sans-serif")
# edge weight labels
# edge_labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)

ax = plt.gca()
ax.margins(0.08)
plt.axis("off")
plt.tight_layout()
plt.savefig('foo.png', bbox_inches='tight', dpi=1200)
# plt.show()