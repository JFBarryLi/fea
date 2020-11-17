import numpy as np
from fea.truss.truss import Truss

mat_prop = {
    'ele1': {'index': 0, 'E': 2000000, 'A': 2},
    'ele2': {'index': 1, 'E': 2000000, 'A': 2},
    'ele3': {'index': 2, 'E': 2000000, 'A': 1},
    'ele4': {'index': 3, 'E': 2000000, 'A': 1}
}

nodal_coords = {
    'node1': {'index': 0, 'x': 0, 'y': 0, 'z': 0},
    'node2': {'index': 1, 'x': 100, 'y': 0, 'z': 0},
    'node3': {'index': 2, 'x': 50, 'y': 50, 'z': 0},
    'node4': {'index': 3, 'x': 200, 'y': 100, 'z': 0}
}

connectivity = {
    'ele1': {'index': 0, 'i': 'node1', 'j': 'node3'},
    'ele2': {'index': 1, 'i': 'node3', 'j': 'node2'},
    'ele3': {'index': 2, 'i': 'node3', 'j': 'node4'},
    'ele4': {'index': 3, 'i': 'node2', 'j': 'node4'}
}

force_vector = {
    'node4': {
        'index': 3,
        'forces': {
            'u1': {'index': 0, 'value': 0},
            'u2': {'index': 1, 'value': -1000},
            'u3': {'index': 2, 'value': 0}
        }
    }
}

boundary_conditions = {
    'node1': {
        'index': 0,
        'bc': {
            'u1': {'index': 0, 'value': 0},
            'u2': {'index': 1, 'value': 0},
            'u3': {'index': 2, 'value': 0}
        }
    },
    'node2': {
        'index': 1,
        'bc': {
            'u1': {'index': 0, 'value': 0},
            'u2': {'index': 1, 'value': 0},
            'u3': {'index': 2, 'value': 0}
        }
    },
    'node3': {
        'index': 2,
        'bc': {
            'u3': {'index': 2, 'value': 0}
        }
    },
    'node4': {
        'index': 3,
        'bc': {
            'u3': {'index': 2, 'value': 0}
        }
    }
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
        'node1': {'index': 0, 'x': 0, 'y': 0, 'z': 0},
        'node2': {'index': 1, 'x': 100, 'y': 0, 'z': 0},
        'node3': {'index': 2, 'x': 50, 'y': 50, 'z': 0},
        'node4': {'index': 3, 'x': 200, 'y': 100, 'z': 0}
    }


def test_truss_create_nodes():
    t.create_nodes()
    assert t.nodes['node2'].x == 100


def test_truss_create_elements():
    t.create_elements()
    assert t.elements['ele1'].nodej.y == 50
    assert (np.round(t.elements['ele1'].K) == np.array([
        [ 28284,  28284,  0, -28284, -28284, 0],
        [ 28284,  28284,  0, -28284, -28284, 0],
        [     0,      0,  0,      0,      0, 0],
        [-28284, -28284 ,  0,  28284,  28284, 0],
        [-28284, -28284,  0,  28284,  28284, 0],
        [     0,      0,  0,      0,      0, 0]
    ])).all()


def test_truss_assemblage():
    t.assemblage()
    assert np.equal(np.round(t.K), np.array([
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
    assert np.equal(np.round(t.Q, 4), np.array([
        [      0],
        [      0],
        [      0],
        [      0],
        [      0],
        [      0],
        [ 0.0265],
        [ 0.0088],
        [      0],
        [ 0.3479],
        [-0.5600],
        [      0]
    ])).all()


def test_truss_stress():
    t.stress()
    assert {
        key: round(t.stresses[key], 1) for key in t.stresses
    } == {
        'ele1': 707.1,
        'ele2': -353.6,
        'ele3': 1581.1,
        'ele4': -2121.3
    }


def test_calculate_deformed_nodal_coords():
    t.calculate_deformed_nodal_coords()
    assert {
        key:
            {
                k: round(
                    t.deformed_nodal_coords[key][k],
                    4
                ) for k in t.deformed_nodal_coords[key]
            }
            for key in t.deformed_nodal_coords
    } == {
        'node1': {'index': 0, 'x': 0.0, 'y': 0.0, 'z': 0.0},
        'node2': {'index': 1, 'x': 100.0, 'y': 0.0, 'z': 0.0},
        'node3': {'index': 2, 'x': 50.0265, 'y': 50.0088, 'z': 0.0},
        'node4': {'index': 3, 'x': 200.3479, 'y': 99.4400, 'z': 0.0}
    }


def test_solve_truss():
    t2 = Truss(
        mat_prop,
        nodal_coords,
        connectivity,
        force_vector,
        boundary_conditions
    )
    t2.solve_truss()

    assert {
        key:
            {
                k: round(
                    t2.deformed_nodal_coords[key][k],
                    4
                ) for k in t2.deformed_nodal_coords[key]
            }
            for key in t2.deformed_nodal_coords
    } == {
        'node1': {'index': 0, 'x': 0.0, 'y': 0.0, 'z': 0.0},
        'node2': {'index': 1, 'x': 100.0, 'y': 0.0, 'z': 0.0},
        'node3': {'index': 2, 'x': 50.0265, 'y': 50.0088, 'z': 0.0},
        'node4': {'index': 3, 'x': 200.3479, 'y': 99.4400, 'z': 0.0}
    }
