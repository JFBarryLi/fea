from fea.truss.node import Node


def test_node_init():
    n = Node(1, 1, 2, 3)
    assert n.id == 1
    assert n.x == 1
    assert n.y == 2
    assert n.z == 3
