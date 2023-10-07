import csv
import networkx as nx
from networkx.algorithms import community as nxc
import numpy as np


def from_csv(input: str) -> nx.Graph:
    """Populate a un-directed graph from a CSV file.

    The input CSV requires a `source` field and a `target` field to build up the graph.
    """
    G = nx.Graph()

    with open(input, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_nodes_from([row["source"], row["target"]])
            G.add_edge(row["source"], row["target"])

    return G


def directed_from_csv(input: str) -> nx.DiGraph:
    """Populate a directed graph from a CSV file.

    The input CSV requires a `source` field and a `target` field to build up the graph.
    """
    G = nx.DiGraph()

    with open(input, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            G.add_nodes_from([row["source"], row["target"]])
            G.add_edge(row["source"], row["target"])

    return G


def count_nodes(G: nx.Graph or nx.DiGraph) -> int:
    """Count the number of nodes in a graph."""
    return G.number_of_nodes()


def count_edges(G: nx.Graph or nx.DiGraph) -> int:
    """Count the numbers of edges in a graph."""
    return G.number_of_edges()


def avg_node_degree(G: nx.Graph or nx.DiGraph) -> float:
    """Calculate the average node degree of a graph."""
    return np.mean([d for _, d in G.degree()])


def density(G: nx.Graph or nx.DiGraph) -> float:
    """Calculate the graph density."""
    return nx.density(G)


def degree_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a graph."""
    return nx.degree_centrality(G)


def degree_in_centrality(G: nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a directed graph."""
    return nx.degree_centrality_in(G)


def degree_out_centrality(G: nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a directed graph."""
    return nx.degree_centrality_out(G)


def betweenness_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the betweenness centrality of every node in a graph."""
    return nx.betweenness_centrality(G)


def closeness_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the closeness centrality of every node in a graph."""
    return nx.closeness_centrality(G)


def eigenvector_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the eigenvector centrality of every node in a graph."""
    return nx.eigenvector_centrality(G)


def k_clique_communities(G: nx.Graph or nx.DiGraph, k: int) -> list:
    """Find k-clique communities in graph using the percolation method.

    A k-clique community is the union of all cliques of size k that can be
    reached through adjacent (sharing k-1 nodes) k-cliques."""
    return list(nxc.k_clique_communities(G, k))


def louvain_communities(G: nx.Graph or nx.DiGraph, k: int) -> list:
    """Find the best partition of a graph using the Louvain Community Detection
    Algorithm.

    Louvain Community Detection Algorithm is a simple method to extract the
    community structure of a network. This is a heuristic method based on
    modularity optimization."""
    return list(nxc.louvain_communities(G, k))
