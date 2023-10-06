import click
from .graph import (
    from_csv,
    directed_from_csv,
    count_nodes,
    count_edges,
    avg_node_degree,
    density,
)
from .host import write_to_file
from .plot import graph_render


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
