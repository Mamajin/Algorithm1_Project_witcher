import csv
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)

    def add_edge(self, source, target, weight, book):
        edge = {'target': target, 'weight': weight, 'book': book}
        self.adj_list[source].append(edge)
        # Assuming undirected graph, adding reverse edge as well
        reverse_edge = {'target': source, 'weight': weight, 'book': book}
        self.adj_list[target].append(reverse_edge)

    def degree_centrality(self):
        centrality = {}
        for node in self.adj_list:
            centrality[node] = sum(edge['weight'] for edge in self.adj_list[node])
        return centrality


# Create an instance of the Graph class
graph = Graph()

# Load data from CSV file and populate the graph
with open('witcher_network.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        source = row['Source']
        target = row['Target']
        weight = int(row['Weight'])
        book = int(row['book'])
        graph.add_edge(source, target, weight, book)

# Calculate degree centrality
degree_centrality = graph.degree_centrality()

# Sort nodes by degree centrality and select top 30
top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]

# Print top 30 characters by degree centrality
print("Top 30 Characters by Degree Centrality:")
for node, centrality in top_nodes:
    print(f"{node}: {centrality}")


# Sort nodes by degree centrality and select top 30
top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:30]
top_characters = [node for node, centrality in top_nodes]

# Create a subgraph containing only the top characters and their interactions
subgraph_edges = [(source, target, data) for source, edges in graph.adj_list.items()
                  for edge in edges
                  for target, data in [(edge['target'], {'weight': edge['weight'], 'book': edge['book']})]
                  if source in top_characters and target in top_characters]
subgraph = nx.Graph()
subgraph.add_edges_from(subgraph_edges)

# Calculate node positions for visualization
pos = nx.spring_layout(subgraph)

# Draw the graph
plt.figure(figsize=(12, 8))
nx.draw(subgraph, pos, with_labels=True, node_size=500, node_color='skyblue', edge_color='gray', width=1.5, font_size=10)
plt.title('Character Interaction Network (Top 30 Characters)')

# Save the graph as an image
plt.savefig('top_30_character_interaction_network.png')

# Display the image
plt.show()
