import click
from .graph import (
    build_graph,
    degree_centrality,
    degree_in_centrality,
    degree_out_centrality,
    betweenness_centrality,
    closeness_centrality,
    eigenvector_centrality,
    k_clique_communities,
    louvain_communities,
    label_propagation_communities,
    clustering,
)
from .data import (
    compute_basic_topology,
    map_directed_degree_centrality,
    map_undirected_degree_centrality,
    map_centrality_neighbours,
    map_centrality_data,
    map_communities,
)
from .host import write_to_file
from .plot import (
    render_graph,
    render_bridges,
    render_centrality_distribution,
    render_centrality_graph,
    render_community,
)
import os
from os.path import join


GRAPH_TYPES = ["directed", "undirected"]


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("all")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument(
    "outdir",
    type=click.Path(writable=True, dir_okay=True, file_okay=False),
    default="out",
)
def all(graph, input, outdir):
    G = build_graph(input, graph)

    os.makedirs(outdir, exist_ok=True)

    # Topology
    topology_basic_file = join(outdir, "topology.csv")
    topology_basic_data = compute_basic_topology(G, graph)
    write_to_file(topology_basic_file, topology_basic_data)

    graph_plot_file = join(outdir, "graph.png")
    render_graph(G, graph_plot_file)

    if graph == "undirected":
        bridges_plot_file = join(outdir, "bridges.png")
        render_bridges(G, bridges_plot_file)

    # Degree Centrality
    centrality_degree_file = join(outdir, "centrality-degree.csv")
    centrality_degree_neighbours_file = join(outdir, "centrality-degree-neighbours.csv")
    centrality_degree_plot_file = join(outdir, "degree-centrality.png")
    centrality_degree_neighbours_plot_file = join(
        outdir, "degree-centrality-distribution.png"
    )
    centrality_degree_data = degree_centrality(G)
    if graph == "undirected":
        write_to_file(
            centrality_degree_file,
            map_undirected_degree_centrality(centrality_degree_data),
        )
    elif graph == "undirected":
        centrality_degree_in_data = degree_in_centrality(G)
        centrality_degree_out_data = degree_out_centrality(G)
        write_to_file(
            centrality_degree_file,
            map_directed_degree_centrality(
                centrality_degree_data,
                centrality_degree_in_data,
                centrality_degree_out_data,
            ),
        )

    write_to_file(
        centrality_degree_neighbours_file,
        map_centrality_neighbours(
            sorted(G.degree, key=lambda item: item[1], reverse=True)
        ),
    )
    render_centrality_graph(G, centrality_degree_data, centrality_degree_plot_file)
    render_centrality_distribution(
        centrality_degree_data,
        centrality_degree_neighbours_plot_file,
        title="Degree Centrality Histogram",
    )

    # Betweenness Centrality
    centrality_betweenness_file = join(outdir, "centrality-betweenness.csv")
    centrality_betweenness_plot_file = join(outdir, "betweenness-centrality.png")
    centrality_betweenness_distribution_plot_file = join(
        outdir, "betweenness-centrality-distribution.png"
    )

    centrality_betweenness_data = betweenness_centrality(G)
    write_to_file(
        centrality_betweenness_file,
        map_centrality_data(centrality_betweenness_data, "betweenness"),
    )

    render_centrality_distribution(
        centrality_betweenness_data,
        centrality_betweenness_distribution_plot_file,
        title="Betweenness Centrality Histogram",
    )
    render_centrality_graph(
        G,
        centrality_betweenness_data,
        centrality_betweenness_plot_file,
        size_multiplier=1200,
    )

    # Eigenvector Centrality
    centrality_eigenvector_file = join(outdir, "centrality-eigenvector.csv")
    centrality_eigenvector_plot_file = join(outdir, "eigenvector-centrality.png")
    centrality_eigenvector_distribution_plot_file = join(
        outdir, "eigenvector-centrality-distribution.png"
    )

    centrality_eigenvector_data = eigenvector_centrality(G)
    write_to_file(
        centrality_eigenvector_file,
        map_centrality_data(centrality_eigenvector_data, "eigenvector"),
    )

    render_centrality_distribution(
        centrality_eigenvector_data,
        centrality_eigenvector_distribution_plot_file,
        title="Eigenvector Centrality Histogram",
    )
    render_centrality_graph(
        G,
        centrality_eigenvector_data,
        centrality_eigenvector_plot_file,
        size_multiplier=4000,
    )

    # Closeness Centrality
    centrality_closeness_file = join(outdir, "centrality-closeness.csv")
    centrality_closeness_plot_file = join(outdir, "closeness-centrality.png")
    centrality_closeness_distribution_plot_file = join(
        outdir, "closeness-centrality-distribution.png"
    )

    centrality_closeness_data = closeness_centrality(G)
    write_to_file(
        centrality_closeness_file,
        map_centrality_data(centrality_closeness_data, "closeness"),
    )

    render_centrality_distribution(
        centrality_closeness_data,
        centrality_closeness_distribution_plot_file,
        title="Closeness Centrality Histogram",
    )
    render_centrality_graph(
        G,
        centrality_closeness_data,
        centrality_closeness_plot_file,
        size_multiplier=50,
    )

    # Clustering
    clustering_distribution_plot_file = join(outdir, "clustering-distribution.png")
    clustering_data = clustering(G)
    render_centrality_distribution(
        clustering_data,
        clustering_distribution_plot_file,
        title="Clustering Histogram",
    )


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
    G = build_graph(input, graph)
    data = compute_basic_topology(G, graph)
    write_to_file(output, data)


@cli.group()
@click.pass_context
def plot(ctx):
    pass


@plot.command("graph")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="graph.png")
def plot_graph(graph, iterations, input, output):
    G = build_graph(input, graph)

    render_graph(G, output, iterations)


@plot.command("bridges")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="bridges.png")
def plot_bridges(graph, iterations, input, output):
    G = build_graph(input, graph)

    render_bridges(G, output, iterations)


@plot.command("degree-centrality-distribution")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.option("--bins", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument(
    "output",
    type=click.Path(writable=True),
    default="degree-centrality-distribution.png",
)
def plot_degree_centrality_distribution(graph, iterations, bins, input, output):
    G = build_graph(input, graph)

    data = degree_centrality(G)
    render_centrality_distribution(
        data, output, title="Degree Centrality Histogram", bins=bins
    )


@plot.command("betweenness-centrality-distribution")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.option("--bins", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument(
    "output",
    type=click.Path(writable=True),
    default="betweenness-centrality-distribution.png",
)
def plot_betweenness_centrality_distribution(graph, iterations, bins, input, output):
    G = build_graph(input, graph)

    data = betweenness_centrality(G)
    render_centrality_distribution(
        data, output, title="Betweenness Centrality Histogram", bins=bins
    )


@plot.command("eigenvector-centrality-distribution")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.option("--bins", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument(
    "output",
    type=click.Path(writable=True),
    default="eigenvector-centrality-distribution.png",
)
def plot_eigenvector_centrality_distribution(graph, iterations, bins, input, output):
    G = build_graph(input, graph)

    data = eigenvector_centrality(G)
    render_centrality_distribution(
        data, output, title="Eigenvector Centrality Histogram", bins=bins
    )


@plot.command("closeness-centrality-distribution")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.option("--bins", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument(
    "output",
    type=click.Path(writable=True),
    default="closeness-centrality-distribution.png",
)
def plot_closeness_centrality_distribution(graph, iterations, bins, input, output):
    G = build_graph(input, graph)

    data = closeness_centrality(G)
    render_centrality_distribution(
        data, output, title="Closeness Centrality Histogram", bins=bins
    )


@plot.command("label-propagation-community")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.option("--iterations", type=int, default=15)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="graph.png")
def plot_label_propagation_community(graph, iterations, input, output):
    G = build_graph(input, graph)
    communities = label_propagation_communities(G)

    render_community(G, communities, output, iterations)


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
    G = build_graph(input, graph)

    centrality_degree_data = degree_centrality(G)

    if graph == "undirected":
        data = map_undirected_degree_centrality(centrality_degree_data)
    elif graph == "undirected":
        centrality_degree_in_data = degree_in_centrality(G)
        centrality_degree_out_data = degree_out_centrality(G)

        data = map_directed_degree_centrality(
            centrality_degree_data,
            centrality_degree_in_data,
            centrality_degree_out_data,
        )

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
    G = build_graph(input, graph)

    centrality = betweenness_centrality(G)

    data = map_centrality_data(centrality, "betweenness")

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
    G = build_graph(input, graph)

    centrality = closeness_centrality(G)

    data = map_centrality_data(centrality, "closeness")

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
    G = build_graph(input, graph)

    centrality = eigenvector_centrality(G)

    data = map_centrality_data(centrality, "eigenvector")

    write_to_file(output, data)


@cli.group()
@click.pass_context
def community(ctx):
    pass


@community.command("k-clique")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(["undirected"]),
    default="undirected",
)
@click.option("-k", type=int, default=100)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def communities_k_clique(graph, k, input, output):
    G = build_graph(input, graph)

    communities = k_clique_communities(G, k)

    data = map_communities(communities)

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
    G = build_graph(input, graph)

    communities = louvain_communities(G, k)

    data = map_communities(communities)

    write_to_file(output, data)


@community.command("label-propagation")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def communities_label_propagation(graph, input, output):
    G = build_graph(input, graph)

    communities = label_propagation_communities(G)
    data = map_communities(communities)

    write_to_file(output, data)
