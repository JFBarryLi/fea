from fea.truss.truss import Truss

# TODO: Find a textbook example to use as test cases.
mat_prop = {1: {'E': 1, 'A': 1}}
nodal_coords = {1: {'x': 0, 'y': 0, 'z': 0}, 2: {'x': 3, 'y': 4, 'z': 0}}
connectivity = {1: {'i': 1, 'j': 2}}
force_vector = {}
boundary_conditions = {}

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
        2: {'x': 3, 'y': 4, 'z': 0}
    }


def test_truss_create_nodes():
    t.create_nodes()
    assert t.nodes[1].x == 0


def test_truss_create_elements():
    t.create_elements()
    assert t.elements[1]


def test_truss_assemblage():
    t.assemblage()
    assert t.K.any()


def test_truss_displacement():
    pass


def test_truss_stress():
    pass
