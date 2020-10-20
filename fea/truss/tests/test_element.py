from fea.truss.element import Element
from fea.truss.node import Node
import numpy as np


def test_element_init():
    ni = Node(1, 0, 0, 0)
    nj = Node(2, 3, 4, 0)
    ele = Element(1, ni, nj, {'E': 10, 'A': 10})
    assert ele.L == 5
    assert ele.Cx == 3/5
    assert ele.Cy == 4/5
    assert ele.Cz == 0


def test_element_stiffness():
    ni = Node(1, 0, 0, 0)
    nj = Node(2, 500, 500, 0)
    ele = Element(1, ni, nj, {'E': 20000, 'A': 200})
    ele.stiffness()
    assert (np.round(ele.K) == np.array([
        [ 2828,  2828,  0, -2828, -2828, 0],
        [ 2828,  2828,  0, -2828, -2828, 0],
        [    0,     0,  0,     0,     0, 0],
        [-2828, -2828,  0,  2828,  2828, 0],
        [-2828, -2828,  0,  2828,  2828, 0],
        [    0,     0,  0,     0,     0, 0]
    ])).all()
