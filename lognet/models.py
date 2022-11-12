from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Hashable

from .helpers import export_data, import_data


class NodeType(Enum):
    PLANT = 'PLANT'
    DC = 'DC'
    WAREHOUSE = 'WAREHOUSE'
    CLIENT = 'CLIENT'


@dataclass
class Node:
    type: NodeType
    capacity: int
    cost: int = 0

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = NodeType[self.type]


@dataclass
class Connection:
    from_node: Hashable
    to_node: Hashable
    capacity: int
    cost: int


def config_to_nodes_connections(
        config: dict
) -> (dict[Hashable, Node], list[Connection]):
    nodes = {i: Node(**j) for i, j in config['nodes'].items()}
    connections = [Connection(**i) for i in config['connections']]
    return nodes, connections


class Network:
    def __init__(
            self,
            nodes: dict[Hashable, Node],
            connections: list[Connection]
    ):
        self.nodes = nodes or {}
        self.connections = connections or {}

    def add_node(self, id_: str, node: Node):
        self.nodes[id_] = node

    def remove_node(self, id_: str):
        if id_ in self.nodes:
            del self.nodes[id_]

    def add_connection(
            self,
            from_node: Hashable,
            to_node: Hashable,
            connection: Connection
    ):
        self.connections[(from_node, to_node)] = connection

    def remove_connection(self, from_node: Hashable, to_node: Hashable):
        if k := (from_node, to_node) in self.connections:
            del self.connections[k]

    @property
    def plant_nodes(self) -> tuple[tuple[Hashable, Node]]:
        return tuple(filter(  # noqa
            lambda n: n[1].type == NodeType.PLANT,
            self.nodes.items()
        ))

    @property
    def client_nodes(self) -> tuple[tuple[Hashable, Node]]:
        return tuple(filter(  # noqa
            lambda n: n[1].type == NodeType.CLIENT,
            self.nodes.items()
        ))

    @property
    def middle_nodes(self) -> tuple[tuple[Hashable, Node]]:
        return tuple(filter(  # noqa
            lambda n: n[1].type in (NodeType.DC, NodeType.WAREHOUSE),
            self.nodes.items()
        ))

    @classmethod
    def from_file(cls, filename: str):
        config = import_data(filename)
        nodes, connections = cls.config_to_nodes_connections(
            config
        )
        return cls(nodes, connections)

    @staticmethod
    def config_to_nodes_connections(
            config: dict
    ) -> (dict[Hashable, Node], list[Connection]):
        nodes = {i: Node(**j) for i, j in config['nodes'].items()}
        connections = [Connection(**i) for i in config['connections']]
        return nodes, connections


class Solution:
    def __init__(
            self,
            nodes: dict[Hashable, Node],
            connections: list[Connection],
            resulting_nodes: dict[Hashable, bool],
            resulting_connections: dict[tuple[Hashable, Hashable], int],
            total_costs: float,
    ):
        self.nodes = deepcopy(nodes)
        self.connections = deepcopy(connections)
        self.resulting_nodes = resulting_nodes
        self.resulting_connections = resulting_connections
        self.total_costs = total_costs

    @property
    def as_dict(self):
        nodes = {}
        for node_id, opened in self.resulting_nodes.items():
            nodes[node_id] = {
                'opened': opened,
                'type': self.nodes[node_id].type.value,
                'capacity': self.nodes[node_id].cost,
                'cost': self.nodes[node_id].capacity,
            }
        connections = []
        for c in self.connections:
            connections.append({
                'from_node': c.from_node,
                'to_node': c.to_node,
                'capacity': c.capacity,
                'cost': c.cost,
                'traffic': self.resulting_connections[
                    (c.from_node, c.to_node)
                ]
            })
        return {
            'total_costs': self.total_costs,
            'nodes': nodes,
            'connections': connections,
        }

    def to_file(self, filename: str):
        export_data(filename, self.as_dict)
