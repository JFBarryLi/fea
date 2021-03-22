![CI](https://github.com/JFBarryLi/fea/actions/workflows/ci.yml/badge.svg)

[<img alt='barryFEA' src='https://user-images.githubusercontent.com/40674314/103185896-77f37f80-488c-11eb-8dff-30caed3e9723.png'>](https://fea.barryli.ca/)

Finite Element Analysis

fea-app is a Python package aimed to use finite element analysis to solve physical problems.

## Installation

```bash
pip install git+https://github.com/JFBarryLi/fea-app.git
```

## Local Development

```bash
git clone https://github.com/JFBarryLi/fea-app.git
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Testing
```bash
make test
```

## Usage

### Truss Solver

```Python
from fea.truss.truss import Truss

mat_prop = {
    'ele1': {'E': 2000000, 'A': 2},
    'ele2': {'E': 2000000, 'A': 2},
    'ele3': {'E': 2000000, 'A': 1},
    'ele4': {'E': 2000000, 'A': 1},
}

nodal_coords = {
    'node1': {'x': 0, 'y': 0, 'z': 0},
    'node2': {'x': 100, 'y': 0, 'z': 0},
    'node3': {'x': 50, 'y': 50, 'z': 0},
    'node4': {'x': 200, 'y': 100, 'z': 0},
}

connectivity = {
    'ele1': {'i': 'node1', 'j': 'node3'},
    'ele2': {'i': 'node3', 'j': 'node2'},
    'ele3': {'i': 'node3', 'j': 'node4'},
    'ele4': {'i': 'node2', 'j': 'node4'},
}

force_vector = [
    {'node': 'node4', 'u1': 0, 'u2': -1000, 'u3': 0},
]

boundary_conditions = [
    {'node': 'node1', 'u1': True, 'u2': True, 'u3': True},
    {'node': 'node2', 'u1': True, 'u2': True, 'u3': True},
    {'node': 'node3', 'u1': False, 'u2': False, 'u3': True},
    {'node': 'node4', 'u1': False, 'u2': False, 'u3': True},
]

t = Truss(
    mat_prop,
    nodal_coords,
    connectivity,
    force_vector,
    boundary_conditions
)

t.solve_truss()
t.stresses
t.deformed_nodal_coords
```

### Api

```shell
make run-api
```

To view the schema

```Python
from rich import print
from api.routers.truss import TrussData

print(TrussData.schema())
```

To view api docs open your browser at <a href="http://localhost:8000/docs" class="external-link" target="_blank">http://localhost:8000/docs</a>.

## Build

```shell
make build
```

## License
See [LICENSE](./LICENSE) for more information.
