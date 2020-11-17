# fea-app

fea-app is a Python package aimed to use finite element analysis to solve physical problems.

Currently implemented solvers are:
- Truss

Solvers that are on the immediate todo:
- Frame
- Plate
- 3D Elements

## Installation

```shell
pip install git+https://github.com/JFBarryLi/fea-app.git
```

### Local Development

```shell
git clone https://github.com/JFBarryLi/fea-app.git
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Truss Solver

```Python
from fea.truss.truss import Truss

mat_prop = {
    'ele1': {'index': 0, 'E': 2000000, 'A': 2},
}

nodal_coords = {
    'node1': {'index': 0, 'x': 0, 'y': 0, 'z': 0},
    'node2': {'index': 1, 'x': 0, 'y': 100, 'z': 0},
}

connectivity = {
    'ele1': {'index': 0, 'i': 'node1', 'j': 'node2'},
}

force_vector = {
    'node2': {
        'index': 1,
        'forces': {
            'u2': {'index': 1, 'value': -10000},
        }
    }
}

boundary_conditions = {
    'node1': {
        'index': 0,
        'bc': {
            'u1': {'index': 0, 'value': 0},
            'u2': {'index': 1, 'value': 0},
            'u3': {'index': 2, 'value': 0},
        }
    },
    'node2': {
        'index': 1,
        'bc': {
            'u1': {'index': 0, 'value': 0},
            'u3': {'index': 2, 'value': 0},
        }
    },
}

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

To view api docs open your browser at <a href="http://localhost/docs" class="external-link" target="_blank">http://localhost/docs</a>.

## Build

```shell
make build
```
