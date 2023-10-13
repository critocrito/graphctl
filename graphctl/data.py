from .graph import (
    from_csv,
    directed_from_csv,
    count_nodes,
    count_edges,
    avg_node_degree,
    density,
    assortativity,
    is_connected,
    is_weakly_connected,
    is_strongly_connected,
    count_connected_components,
    count_weakly_connected_components,
    count_strongly_connected_components,
    avg_clustering,
    count_triangles,
    avg_triangles,
    median_triangles,
    has_bridges,
    count_bridges,
    count_local_bridges,
    stats_components,
    degree_centrality,
    degree_in_centrality,
    degree_out_centrality,
    betweenness_centrality,
    closeness_centrality,
    eigenvector_centrality,
    k_clique_communities,
    louvain_communities,
)
from .utils import float_str
import networkx as nx


def compute_basic_topology(G: nx.Graph or nx.DiGraph, graph) -> list[dict]:
    data = []

    data.append({"measure": "Number of Nodes", "value": count_nodes(G)})
    data.append({"measure": "Number of Edges", "value": count_edges(G)})
    data.append({"measure": "Average Degree of Node", "value": avg_node_degree(G)})
    data.append({"measure": "Graph Density", "value": density(G)})
    data.append({"measure": "Average Clustering", "value": avg_clustering(G)})
    data.append({"measure": "Degree Assortativity", "value": assortativity(G)})

    if graph == "undirected":
        data.append(
            {
                "measure": "Count of Unique Triangles in the Network",
                "value": int(count_triangles(G)),
            }
        )
        data.append(
            {
                "measure": "Average Triangles a Node is part of",
                "value": avg_triangles(G),
            }
        )
        data.append(
            {
                "measure": "Median Triangles a Node is part of",
                "value": median_triangles(G),
            }
        )
        data.append({"measure": "Has Bridges?", "value": has_bridges(G)})
        data.append({"measure": "Count Bridges", "value": count_bridges(G)})
        data.append({"measure": "Count Local Bridges", "value": count_local_bridges(G)})
        data.append({"measure": "Is Connected?", "value": is_connected(G)})
        data.append(
            {"measure": "Number of Components", "value": count_connected_components(G)}
        )

        components = stats_components(G)

        for component in components:
            id = component["id"]

            data.append(
                {
                    "measure": f"Number of Nodes (component {id})",
                    "value": component["count_nodes"],
                }
            )
            data.append(
                {
                    "measure": f"Number of Edges (component {id})",
                    "value": component["count_edges"],
                }
            )
            data.append(
                {
                    "measure": f"Diameter (component {id})",
                    "value": component["diameter"],
                }
            )
            data.append(
                {
                    "measure": f"Average Path (component {id})",
                    "value": component["average_path"],
                }
            )

    if graph == "directed":
        data.append(
            {"measure": "Is Weakly Connected?", "value": is_weakly_connected(G)}
        )
        data.append(
            {"measure": "Is Strongly Connected?", "value": is_strongly_connected(G)}
        )
        data.append(
            {
                "measure": "Number of Strongly Components",
                "value": count_strongly_connected_components(G),
            }
        )
        data.append(
            {
                "measure": "Number of Weakly Components",
                "value": count_weakly_connected_components(G),
            }
        )

    return data


def map_undirected_degree_centrality(centrality_data: dict) -> list:
    centrality_data = sorted(
        centrality_data.items(), key=lambda item: item[1], reverse=True
    )

    data = []

    for i, (k, v) in enumerate(centrality_data):
        data.append({"position": i + 1, "node": k, "degree": float_str(v)})

    return data


def map_directed_degree_centrality(
    centrality_data: dict, centrality_data_in: dict, centrality_data_out: dict
) -> list:
    centrality_data = sorted(
        centrality_data.items(), key=lambda item: item[1], reverse=True
    )

    data = []

    for i, (k, v) in enumerate(centrality_data):
        d = {
            "position": i + 1,
            "node": k,
            "degree": float_str(v),
            "in_degree": float_str(centrality_data_in[k]),
            "out_degree": float_str(centrality_data_out[k]),
        }

        data.append(d)

    return data


def map_centrality_neighbours(degree_data):
    degree_data = sorted(degree_data, key=lambda item: item[1], reverse=True)

    data = []

    for i, (k, v) in enumerate(degree_data):
        d = {"position": i + 1, "node": k, "count_neighbours": float_str(v)}

        data.append(d)

    return data


def map_centrality_data(centrality_data, name):
    centrality_data = sorted(
        centrality_data.items(), key=lambda item: item[1], reverse=True
    )

    data = []

    for i, (k, v) in enumerate(centrality_data):
        data.append({"position": i + 1, "node": k, f"{name}": float_str(v)})

    return data


def map_communities(community_data):
    data = []

    for idx, c in enumerate(community_data):
        count = len(c)
        for n in c:
            data.append({"community": idx, "count": count, "node": n})

    return data
