from typing import Hashable

import matplotlib.pyplot as plt
import networkx as nx

from .models import NodeType, Solution


def draw_graph(
        solution: Solution,
        *,
        filename: str = None,
        pos: dict[Hashable, tuple[float, float]] = None,
        dpi: int = 300,
        figsize: tuple[int, int] = None
):
    G = nx.DiGraph()

    G.add_nodes_from([node_id for node_id in solution.nodes])
    G.add_edges_from(
        [(conn.from_node, conn.to_node) for conn in solution.connections]
    )

    if pos is None:
        pos = {}
        plants = list(filter(
            lambda i: i[1].type == NodeType.PLANT,
            solution.nodes.items()
        ))
        dcs = list(filter(
            lambda i: i[1].type == NodeType.DC,
            solution.nodes.items()
        ))
        warehouses = list(filter(
            lambda i: i[1].type == NodeType.WAREHOUSE,
            solution.nodes.items()
        ))
        clients = list(filter(
            lambda i: i[1].type == NodeType.CLIENT,
            solution.nodes.items()
        ))
        for y, (node_id, _) in enumerate(plants, 1):
            pos[node_id] = (
                0,
                (y - len(plants)) / len(plants) + (1 - 1 / len(plants)) * 0.5
            )
        for y, (node_id, _) in enumerate(dcs, 1):
            pos[node_id] = (
                0.25, (y - len(dcs)) / len(dcs) + (1 - 1 / len(dcs)) * 0.5
            )
        for y, (node_id, _) in enumerate(warehouses, 1):
            pos[node_id] = (
                0.5,
                (y - len(warehouses)) / len(warehouses) + (
                            1 - 1 / len(warehouses)) * 0.5
            )
        for y, (node_id, _) in enumerate(clients, 1):
            pos[node_id] = (
                0.75, (y - len(clients)) / len(clients) + (
                            1 - 1 / len(clients)) * 0.5
            )

    _, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.axis('off')

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[i for i, j in solution.resulting_nodes.items() if not j],
        node_color='gray',
        alpha=0.5,
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[i for i, j in solution.resulting_nodes.items() if j],
        node_color='#85C1E9',
        node_size=400
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[
            i for i, j in solution.resulting_connections.items() if j == 0
        ],
        style='dashed',
        edge_color='gray',
        alpha=0.3
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[
            i for i, j in solution.resulting_connections.items() if j > 0
        ],
        edge_color='black'
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels={
            i: f'{i}\n({solution.nodes[i].capacity})'
            for i, j in solution.resulting_nodes.items() if j
        },
        font_color='red',
        font_size=7
    )
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={
            i: j for i, j in solution.resulting_connections.items() if j
        },
    )
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename, bbox_inches='tight')
