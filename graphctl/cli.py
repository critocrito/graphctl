import click
from .graph import (
    from_csv,
    directed_from_csv,
    count_nodes,
    count_edges,
    avg_node_degree,
    density,
    degree_centrality,
    degree_in_centrality,
    degree_out_centrality,
    betweenness_centrality,
    closeness_centrality,
    eigenvector_centrality,
    k_clique_communities,
    louvain_communities,
)
from .host import write_to_file
from .plot import graph_render
from .utils import float_str


GRAPH_TYPES = ["directed", "undirected"]


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.group()
@click.pass_context
def topology(ctx):
    pass


@topology.command("basic")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def topology_basic(graph, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    data = []

    data.append({"measure": "Number of Nodes", "value": count_nodes(G)})
    data.append({"measure": "Number of Edges", "value": count_edges(G)})
    data.append({"measure": "Average Degree of Node", "value": avg_node_degree(G)})
    data.append({"measure": "Graph Density", "value": density(G)})

    write_to_file(output, data)


@topology.command("graph")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=25)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="graph.png")
def topology_graph(graph, input, output, iterations):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    graph_render(G, iterations)


@cli.group()
@click.pass_context
def centrality(ctx):
    pass


@centrality.command("degree")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def centrality_degree(graph, input, output):
    if graph == "undirected":
        G = from_csv(input)
        centrality = degree_centrality(G)
    elif graph == "directed":
        G = directed_from_csv(input)
        centrality = degree_centrality(G)
        in_centrality = degree_in_centrality(G)
        out_centrality = degree_out_centrality(G)

    data = []

    for n in G.nodes:
        d = {
            "node": n,
            "degree": float_str(centrality[n]),
        }

        if graph == "directed":
            d["in_degree"] = float_str(in_centrality[n])
            d["out_degree"] = float_str(out_centrality[n])

        data.append(d)

    write_to_file(output, data)


@centrality.command("betweenness")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def centrality_betweenness(graph, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    centrality = betweenness_centrality(G)

    data = []

    for n in G.nodes:
        data.append(
            {
                "node": n,
                "betweenness": float_str(centrality[n]),
            }
        )

    write_to_file(output, data)


@centrality.command("closeness")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def centrality_closeness(graph, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    centrality = closeness_centrality(G)

    data = []

    for n in G.nodes:
        data.append(
            {
                "node": n,
                "closeness": float_str(centrality[n]),
            }
        )

    write_to_file(output, data)


@centrality.command("eigenvector")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def centrality_eigenvector(graph, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    centrality = eigenvector_centrality(G)

    data = []

    for n in G.nodes:
        data.append(
            {
                "node": n,
                "eigenvector": float_str(centrality[n]),
            }
        )

    write_to_file(output, data)


@cli.group()
@click.pass_context
def community(ctx):
    pass


@community.command("k-clique")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("-k", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def communities_k_clique(graph, k, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    communities = k_clique_communities(G, k)

    data = []

    for idx, c in enumerate(communities):
        count = len(c)
        for n in c:
            data.append({"community": idx, "count": count, "node": n})

    write_to_file(output, data)


@community.command("louvain")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("-k", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def communities_louvain(graph, k, input, output):
    if graph == "undirected":
        G = from_csv(input)
    elif graph == "directed":
        G = directed_from_csv(input)

    communities = louvain_communities(G, k)

    data = []

    for idx, c in enumerate(communities):
        count = len(c)
        for n in c:
            data.append({"community": idx, "count": count, "node": n})

    write_to_file(output, data)
