from ortools.sat.python import cp_model

from .exceptions import NoSolution
from .models import Network, Solution


def solve(network: Network):
    model = cp_model.CpModel()

    X = {id_: model.NewBoolVar(f'x{id_}') for id_ in network.nodes}
    Y = {}

    for conn in network.connections:
        Y[(conn.from_node, conn.to_node)] = model.NewIntVar(
            0,
            conn.capacity,
            f'y{conn.from_node},{conn.to_node}'
        )

    # all client nodes must be "open"
    for node_id, _ in network.client_nodes:
        model.AddExactlyOne(X[node_id])

    # the sum of incoming flows to the client nodes
    # must be equal to the demand
    for node_id, node in network.client_nodes:
        input_connections = list(filter(
            lambda i: i.to_node == node_id, network.connections
        ))
        model.Add(
            sum(Y[(c.from_node, c.to_node)] for c in input_connections)
            == node.capacity * X[node_id]
        )

    # the sum of outgoing flows from the plant nodes
    # must be less than or equal to the production capacity
    for node_id, node in network.plant_nodes:
        output_connections = list(filter(
            lambda i: i.from_node == node_id, network.connections
        ))
        model.Add(
            sum(Y[(c.from_node, c.to_node)] for c in output_connections)
            <= node.capacity * X[node_id]
        )

    # sum of incoming flows for node type "DC" or "WAREHOUSE"
    # must be less than or equal to the capacity of the node
    for node_id, node in network.middle_nodes:
        related_connections = list(filter(
            lambda i: i.to_node == node_id, network.connections
        ))
        model.Add(
            sum(Y[(c.from_node, c.to_node)] for c in related_connections)
            <= node.capacity * X[node_id]
        )

    # for nodes such as "DC" and "WAREHOUSE" the sum of incoming flows
    # must be equal to the sum of outgoing flows
    for node_id, node in network.middle_nodes:
        input_connections = list(filter(
            lambda i: i.to_node == node_id, network.connections
        ))
        output_connections = list(filter(
            lambda i: i.from_node == node_id, network.connections
        ))
        model.Add(
            sum(Y[(c.from_node, c.to_node)] for c in input_connections)
            == sum(Y[(c.from_node, c.to_node)] for c in output_connections)
        )

    objective = []
    for node_id, node in network.nodes.items():
        objective.append(X[node_id] * node.cost)
    for conn in network.connections:
        objective.append(Y[(conn.from_node, conn.to_node)] * conn.cost)

    # objective function: minimize the cost
    # of maintaining nodes and connections
    model.Minimize(sum(objective))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise NoSolution('no solution')

    resulting_nodes = {id_: solver.BooleanValue(x) for id_, x in X.items()}
    resulting_connections = {
        (n_from, n_to): solver.Value(conn) for
        (n_from, n_to), conn in Y.items()
    }
    return Solution(
        network.nodes,
        network.connections,
        resulting_nodes,
        resulting_connections,
        solver.ObjectiveValue()
    )
