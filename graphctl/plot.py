import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from .graph import bridges, local_bridges
from random import randint


def render_graph(G: nx.Graph or nx.DiGraph, output, iterations: int = 15):
    rnd = np.random.RandomState()
    pos = nx.spring_layout(G, iterations=iterations, seed=rnd)
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)

    plt.tight_layout()
    plt.savefig(output, format="PNG", bbox_inches="tight", dpi=300)


def render_community(
    G: nx.Graph or nx.DiGraph, community_data, output, iterations: int = 15
):
    nodes = {}

    for com in community_data:
        # creates random RGB color
        color = "#%06X" % randint(0, 0xFFFFFF)
        # fill colors list with the particular color for the community nodes
        for node in list(com):
            nodes[node] = color

    colors = [nodes[node] for node in G.nodes()]

    rnd = np.random.RandomState()
    pos = nx.spring_layout(G, iterations=iterations, seed=rnd)
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    nx.draw_networkx(
        G, pos=pos, node_size=10, with_labels=False, width=0.15, node_color=colors
    )

    plt.tight_layout()
    plt.savefig(output, format="PNG", bbox_inches="tight", dpi=300)


def render_bridges(G: nx.Graph, output):
    rnd = np.random.RandomState()
    pos = nx.spring_layout(G, iterations=15, seed=rnd)
    plt.figure(figsize=(15, 8))
    nx.draw_networkx(G, pos=pos, node_size=10, with_labels=False, width=0.15)

    # green color for local bridges
    nx.draw_networkx_edges(
        G, pos, edgelist=local_bridges(G), width=0.5, edge_color="lawngreen"
    )

    # red color for bridges
    nx.draw_networkx_edges(G, pos, edgelist=bridges(G), width=0.5, edge_color="r")

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output, format="PNG", bbox_inches="tight", dpi=300)


def render_centrality_distribution(
    data,
    output,
    bins=25,
    title="Centrality Histogram",
    x_label="Centrality",
    ticks=None,
):
    plt.figure(figsize=(15, 8))
    plt.hist(data.values(), bins=bins, edgecolor="black")
    if ticks is not None:
        plt.xticks(ticks=ticks)  # set the x axis ticks
    plt.title(title, fontdict={"size": 35}, loc="center")
    plt.xlabel(x_label, fontdict={"size": 20})
    plt.ylabel("Counts", fontdict={"size": 20})
    plt.tight_layout()
    plt.savefig(output, format="PNG", bbox_inches="tight", dpi=300)


def render_centrality_graph(
    G: nx.Graph or nx.DiGraph, data, output, iterations: int = 15, size_multiplier=1000
):
    rnd = np.random.RandomState()
    pos = nx.spring_layout(G, iterations=iterations, seed=rnd)
    # set up nodes size for a nice graph representation
    node_size = [v * size_multiplier for v in data.values()]
    plt.figure(figsize=(15, 8))
    nx.draw_networkx(G, pos=pos, node_size=node_size, with_labels=False, width=0.15)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(output, format="PNG", bbox_inches="tight", dpi=300)
