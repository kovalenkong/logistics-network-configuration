import argparse
from pprint import pprint

from . import Network, draw_graph, solve


def configure_parser():
    parser = argparse.ArgumentParser(
        description='Configuring the logistics network'
    )

    parser.add_argument(
        'config',
        type=str,
        help='Config filename (yaml, json)'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Output filename (yaml, json)'
    )
    parser.add_argument(
        '-g',
        '--graph',
        type=str,
        help='Filename to save the result as a graph (png, jpg)'
    )
    return parser


def execute(
        config_filename: str,
        output_filename: str = None,
        graph_filename: str = None
):
    network = Network.from_file(config_filename)
    solution = solve(network)
    if output_filename is None:
        pprint(solution.as_dict, sort_dicts=False)
    else:
        solution.to_file(output_filename)
    if graph_filename is not None:
        draw_graph(solution, filename=graph_filename)


if __name__ == '__main__':
    args = configure_parser().parse_args()
    execute(args.config, args.output, args.graph)
