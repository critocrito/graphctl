import csv
import networkx as nx
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
