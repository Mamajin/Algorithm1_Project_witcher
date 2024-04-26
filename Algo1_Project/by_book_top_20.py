import csv
import networkx as nx
from collections import defaultdict
from Top_30 import Graph
import matplotlib.pyplot as plt

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

# Calculate and visualize top 20 characters by degree centrality for each book
for book_num in range(1, 8):
    # Create a new NetworkX graph for the current book
    G = nx.Graph()

    # Add nodes and edges to the NetworkX graph for the current book
    for source, edges in graph.adj_list.items():
        for edge in edges:
            target = edge['target']
            book = edge['book']
            if book == book_num:
                weight = edge['weight']
                G.add_edge(source, target, weight=weight)

    # Calculate degree centrality for the current book
    centrality = nx.degree_centrality(G)

    # Sort nodes by degree centrality and select top 20
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[
                :20]

    # Create a subgraph containing only the top 20 characters and their interactions
    subgraph_edges = [(source, target) for source, edges in
                      graph.adj_list.items()
                      for edge in edges
                      for target, data in [(edge['target'],
                                            {'weight': edge['weight'],
                                             'book': edge['book']})]
                      if
                      source in [node for node, _ in top_nodes] and target in [
                          node for node, _ in top_nodes]]
    subgraph = nx.Graph()
    subgraph.add_edges_from(subgraph_edges)

    # Calculate node positions for visualization
    pos = nx.spring_layout(subgraph)

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(subgraph, pos, with_labels=True, node_size=500,
            node_color='skyblue', edge_color='gray', width=1.5, font_size=10)
    plt.title(f'Top 20 Characters by Degree Centrality for Book {book_num}')

    # Save the figure to a file
    plt.savefig(f'book_{book_num}_top_20_network.png')

    # Close the plot to avoid overlapping figures
    plt.close()