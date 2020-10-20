import numpy as np
from fea.truss.truss import Truss

mat_prop = {
    1: {'E': 2000000, 'A': 2},
    2: {'E': 2000000, 'A': 2},
    3: {'E': 2000000, 'A': 1},
    4: {'E': 2000000, 'A': 1}
}
nodal_coords = {
    1: {'x': 0, 'y': 0, 'z': 0},
    2: {'x': 100, 'y': 0, 'z': 0},
    3: {'x': 50, 'y': 50, 'z': 0},
    4: {'x': 200, 'y': 100, 'z': 0}
}
connectivity = {
    1: {'i': 1, 'j': 3},
    2: {'i': 3, 'j': 2},
    3: {'i': 3, 'j': 4},
    4: {'i': 2, 'j': 4}
}
force_vector = {
    4: {'x': 0, 'y': -1000, 'z': 0}
}
boundary_conditions = {
    1: {'x': 0, 'y': 0, 'z': 0},
    2: {'x': 0, 'y': 0, 'z': 0}
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
        1: {'x': 0, 'y': 0, 'z': 0},
        2: {'x': 100, 'y': 0, 'z': 0},
        3: {'x': 50, 'y': 50, 'z': 0},
        4: {'x': 200, 'y': 100, 'z': 0}
    }


def test_truss_create_nodes():
    t.create_nodes()
    assert t.nodes[2].x == 100


def test_truss_create_elements():
    t.create_elements()
    assert t.elements[1].nodej.y == 50
    assert (np.round(t.elements[1].K) == np.array([
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
    pass


def test_truss_stress():
    pass
