import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def graph_render(G: nx.Graph or nx.DiGraph, iterations: int = 25):
    rnd = np.random.RandomState()
    pos = nx.spring_layout(G, iterations=iterations, seed=rnd)
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    plot_options = {"node_size": 10, "with_labels": False, "width": 0.15}
    nx.draw_networkx(G, pos=pos, ax=ax, **plot_options)

    plt.tight_layout()
    plt.savefig("graph.png", format="PNG", bbox_inches="tight", dpi=300)
