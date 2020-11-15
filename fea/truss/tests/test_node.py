from fea.truss.node import Node


def test_node_init():
    n = Node('node1', 1, 1, 2, 3)
    assert n.id == 'node1'
    assert n.index == 1
    assert n.x == 1
    assert n.y == 2
    assert n.z == 3
