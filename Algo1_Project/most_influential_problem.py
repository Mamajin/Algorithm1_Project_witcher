import csv
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)

    def add_edge(self, source, target, weight, book):
        edge = {'target': target, 'weight': weight, 'book': book}
        self.adjacency_list[source].append(edge)
        # Assuming undirected graph, adding reverse edge as well
        reverse_edge = {'target': source, 'weight': weight, 'book': book}
        self.adjacency_list[target].append(reverse_edge)

    def degree_centrality(self):
        centrality = {}
        for node in self.adjacency_list:
            centrality[node] = sum(edge['weight'] for edge in self.adjacency_list[node])
        return centrality

    def most_influential_character(self):
        degree_centrality = self.degree_centrality()
        return max(degree_centrality, key=degree_centrality.get)

    def visualize_most_influential_character(self, save_path=None):
        most_influential = self.most_influential_character()
        subgraph_edges = [(source, target) for source, edges in self.adjacency_list.items()
                          for edge in edges
                          for target, data in [(edge['target'], {'weight': edge['weight'], 'book': edge['book']})]
                          if source == most_influential or target == most_influential]
        subgraph = nx.Graph()
        subgraph.add_edges_from(subgraph_edges)
        pos = nx.spring_layout(subgraph)
        plt.figure(figsize=(12, 8))
        nx.draw(subgraph, pos, with_labels=True, node_size=500,
                node_color='skyblue', edge_color='gray', width=1.5, font_size=10)
        plt.title(f'Most Influential Character: {most_influential}')
        if save_path:
            plt.savefig(save_path)
        plt.show()

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

# Visualize and save the most influential character graph
save_path = 'most_influential_character_graph.png'
graph.visualize_most_influential_character(save_path)