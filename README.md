# logistics_network_configuration
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)

Configuring logistics networks with constraints programming.

### Installation

```bash
git clone https://github.com/kovalenkong/logistics-network-configuration.git
cd logistics-network-configuration/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Writing a configuration file

The configuration file must contain information about the objects (nodes) of the logistic network
and the connections between them.
Supported file extensions: yaml (yml), json.
The file scheme is available in file `scheme.yaml`.

An example of a simple configuration file `config.yaml` including three nodes and two connections:

```yaml
nodes:
  1:
    type: PLANT
    capacity: 300
    cost: 400
  2:
    type: PLANT
    capacity: 200
    cost: 300
  3:
    type: CLIENT
    capacity: 100

connections:
  - from_node: 1
    to_node: 3
    capacity: 300
    cost: 1
  - from_node: 2
    to_node: 3
    capacity: 200
    cost: 1
```

### Solving problem

```bash
python -m lognet config.yaml
```

The output to the console will be:

```
{'total_costs': 400.0,
 'nodes': {1: {'opened': False, 'type': 'PLANT', 'capacity': 400, 'cost': 300},
           2: {'opened': True, 'type': 'PLANT', 'capacity': 300, 'cost': 200},
           3: {'opened': True, 'type': 'CLIENT', 'capacity': 0, 'cost': 100}},
 'connections': [{'from_node': 1,
                  'to_node': 3,
                  'capacity': 300,
                  'cost': 1,
                  'traffic': 0},
                 {'from_node': 2,
                  'to_node': 3,
                  'capacity': 200,
                  'cost': 1,
                  'traffic': 100}]}
```

The optimal solution is to open the second plant (node #2).

You can also save the results to a separate file (yaml or json format), and keep the visualization of the result
as a graph by passing optional arguments:

```bash
python3 -m lognet config.yaml -o result.yaml -g result.png
```

### Using as a code

```python
from lognet import Network, solve

network = Network.from_file('config.yaml')
solution = solve(network)
```
