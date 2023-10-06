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


GRAPH_TYPES = ["directed", "undirected"]


@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command("topology")
@click.option(
    "-g",
    "--graph",
    type=click.Choice(GRAPH_TYPES),
    default="undirected",
)
@click.argument("input", type=click.Path(exists=True, readable=True))
@click.argument("output", type=click.Path(writable=True), default="out.csv")
def graph_topology(graph, input, output):
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
