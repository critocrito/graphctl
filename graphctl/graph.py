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


def build_graph(input, graph):
    assert graph in [
        "directed",
        "undirected",
    ], f"graph type `{graph}` must be either directed or undirected"

    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

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


def is_connected(G: nx.Graph) -> bool:
    """Returns True if the graph is connected, False otherwise."""
    return nx.is_connected(G)


def is_weakly_connected(G: nx.DiGraph) -> bool:
    """Test directed graph for weak connectivity.

    A directed graph is weakly connected if and only if the graph is connected
    when the direction of the edge between nodes is ignored.

    Note that if a graph is strongly connected (i.e. the graph is connected even
    when we account for directionality), it is by definition weakly connected as
    well.
    """
    return nx.is_weakly_connected(G)


def is_strongly_connected(G: nx.DiGraph) -> bool:
    """Test directed graph for strong connectivity.

    A directed graph is strongly connected if and only if every vertex in the
    graph is reachable from every other vertex.
    """
    return nx.is_strongly_connected(G)


def count_connected_components(G: nx.Graph) -> int:
    """Return the number of connected components."""
    return nx.number_connected_components(G)


def count_strongly_connected_components(G: nx.DiGraph) -> int:
    """Return the number of strongly connected components."""
    return nx.number_strongly_connected_components(G)


def count_weakly_connected_components(G: nx.DiGraph) -> int:
    """Return the number of weakly connected components."""
    return nx.number_weakly_connected_components(G)


def clustering(G: nx.Graph or nx.DiGraph):
    return nx.clustering(G)


def avg_clustering(G: nx.Graph or nx.DiGraph) -> float:
    """Compute the average clustering coefficient for the graph G.

    The closer the average clustering coefficient is to, the more complete the
    graph will be because there’s just one giant component.
    """
    return nx.average_clustering(G)


def count_triangles(G: nx.Graph) -> int:
    triangles_per_node = list(nx.triangles(G).values())

    # divide by 3 because each triangle is counted once for each node
    return sum(triangles_per_node) / 3


def avg_triangles(G: nx.Graph) -> float:
    """The average number of triangles that a node is a part of."""
    triangles_per_node = list(nx.triangles(G).values())

    return np.mean(triangles_per_node)


def median_triangles(G: nx.Graph) -> float:
    """The average number of triangles that a node is a part of."""
    triangles_per_node = list(nx.triangles(G).values())

    return np.median(triangles_per_node)


def has_bridges(G: nx.Graph) -> bool:
    return nx.has_bridges(G)


def bridges(G: nx.Graph) -> list:
    return list(nx.bridges(G))


def local_bridges(G: nx.Graph) -> list:
    return list(nx.local_bridges(G, with_span=False))


def count_bridges(G: nx.Graph) -> int:
    return len(bridges(G))


def count_local_bridges(G: nx.Graph) -> int:
    return len(local_bridges(G))


def shortest_paths(G: nx.Graph):
    shortest_path_lengths = dict(nx.all_pairs_shortest_path_length(G))
    diameter = max(nx.eccentricity(G, sp=shortest_path_lengths).values())
    average_path_lengths = [
        np.mean(list(spl.values())) for spl in shortest_path_lengths.values()
    ]

    return {
        "count_nodes": G.number_of_nodes(),
        "count_edges": G.number_of_edges(),
        "diameter": diameter,
        "average_path": np.mean(average_path_lengths),
    }


def stats_components(G: nx.Graph or nx.DiGraph):
    """Break down the stats of each sub-graph."""
    data = []

    for i, component in enumerate(nx.connected_components(G)):
        S = G.subgraph(component).copy()
        paths = shortest_paths(S)
        paths["id"] = i

        data.append(paths)

    return data


def assortativity(G: nx.Graph or nx.DiGraph) -> float:
    """Assortativity measures the similarity of connections in the graph with
    respect to the node degree."""
    return nx.degree_pearson_correlation_coefficient(G)


def degree_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a graph."""
    return nx.degree_centrality(G)


def count_degree_centrality_neighbours(G: nx.Graph or nx.DiGraph) -> list:
    return sorted(G.degree, key=lambda item: item[1], reverse=True)


def degree_in_centrality(G: nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a directed graph."""
    return nx.in_degree_centrality(G)


def degree_out_centrality(G: nx.DiGraph) -> dict:
    """Calculate the degree centrality of every node in a directed graph."""
    return nx.out_degree_centrality(G)


def betweenness_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the betweenness centrality of every node in a graph."""
    return nx.betweenness_centrality(G)


def closeness_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the closeness centrality of every node in a graph."""
    return nx.closeness_centrality(G)


def eigenvector_centrality(G: nx.Graph or nx.DiGraph) -> dict:
    """Calculate the eigenvector centrality of every node in a graph."""
    return nx.eigenvector_centrality(G)


def k_clique_communities(G: nx.DiGraph, k: int) -> list:
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


def label_propagation_communities(G: nx.Graph or nx.DiGraph) -> list:
    """Generates community sets determined by label propagation

    Finds communities in G using a semi-synchronous label propagation method.
    This method combines the advantages of both the synchronous and asynchronous
    models. Not implemented for directed graphs.
    """
    return nxc.label_propagation_communities(G)
