import numpy as np
from fea.truss.truss import Truss

mat_prop = {
    0: {'E': 2000000, 'A': 2},
    1: {'E': 2000000, 'A': 2},
    2: {'E': 2000000, 'A': 1},
    3: {'E': 2000000, 'A': 1}
}
nodal_coords = {
    0: {'x': 0, 'y': 0, 'z': 0},
    1: {'x': 100, 'y': 0, 'z': 0},
    2: {'x': 50, 'y': 50, 'z': 0},
    3: {'x': 200, 'y': 100, 'z': 0}
}
connectivity = {
    0: {'i': 0, 'j': 2},
    1: {'i': 2, 'j': 1},
    2: {'i': 2, 'j': 3},
    3: {'i': 1, 'j': 3}
}
force_vector = {
    3: {0: 0, 1: -1000, 2: 0}
}
boundary_conditions = {
    0: {0: 0, 1: 0, 2: 0},
    1: {0: 0, 1: 0, 2: 0}
}

t = Truss(
    mat_prop,
    nodal_coords,
    connectivity,
    force_vector,
    boundary_conditions
)


def test_truss_creation():
    assert t.nodal_coords == {
        0: {'x': 0, 'y': 0, 'z': 0},
        1: {'x': 100, 'y': 0, 'z': 0},
        2: {'x': 50, 'y': 50, 'z': 0},
        3: {'x': 200, 'y': 100, 'z': 0}
    }


def test_truss_create_nodes():
    t.create_nodes()
    assert t.nodes[1].x == 100


def test_truss_create_elements():
    t.create_elements()
    assert t.elements[0].nodej.y == 50
    assert (np.round(t.elements[0].K) == np.array([
        [ 28284,  28284,  0, -28284, -28284, 0],
        [ 28284,  28284,  0, -28284, -28284, 0],
        [     0,      0,  0,      0,      0, 0],
        [-28284, -28284,  0,  28284,  28284, 0],
        [-28284, -28284,  0,  28284,  28284, 0],
        [     0,      0,  0,      0,      0, 0]
    ])).all()


def test_truss_assemblage():
    t.assemblage()
    assert (np.round(t.K) == np.array([
        [ 28284,  28284, 0,      0,      0, 0, -28284, -28284, 0,      0,      0, 0],
        [ 28284,  28284, 0,      0,      0, 0, -28284, -28284, 0,      0,      0, 0],
        [     0,      0, 0,      0,      0, 0,      0,      0, 0,      0,      0, 0],
        [     0,      0, 0,  35355, -21213, 0, -28284,  28284, 0,  -7071,  -7071, 0],
        [     0,      0, 0, -21213,  35355, 0,  28284, -28284, 0,  -7071,  -7071, 0],
        [     0,      0, 0,      0,      0, 0,      0,      0, 0,      0,      0, 0],
        [-28284, -28284, 0, -28284,  28284, 0,  67953,   3795, 0, -11384,  -3795, 0],
        [-28284, -28284, 0,  28284, -28284, 0,   3795,  57833, 0,  -3795,  -1265, 0],
        [     0,      0, 0,      0,      0, 0,      0,      0, 0,      0,      0, 0],
        [     0,      0, 0,  -7071,  -7071, 0, -11384,  -3795, 0,  18455,  10866, 0],
        [     0,      0, 0,  -7071,  -7071, 0,  -3795,  -1265, 0,  10866,   8336, 0],
        [     0,      0, 0,      0,      0, 0,      0,      0, 0,      0,      0, 0]
    ])).all()


def test_truss_displacement():
    t.displacement()
    assert t.Q == [1]


def test_truss_stress():
    pass
