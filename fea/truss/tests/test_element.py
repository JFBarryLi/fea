from fea.truss.element import Element
from fea.truss.node import Node


def test_element_init():
    ni = Node(1, 0, 0, 0)
    nj = Node(2, 3, 4, 0)
    ele = Element(1, ni, nj, 10, 10)
    assert ele.L == 5
    assert ele.Cx == 3/5
    assert ele.Cy == 4/5
    assert ele.Cz == 0


def test_element_stiffness():
    pass
