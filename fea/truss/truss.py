import logging
import numpy as np
from .node import Node
from .element import Element

log = logging.getLogger(__name__)


class Truss():
    """
    Truss class, represent simplified model of a truss structure.
    Uniform tubular/circular cross-section and single material elements.

    ...

    Attributes
    ----------
    mat_prop : dict
        Material property dictionary.
        Young's modulus, and cross-sectional area.
    nodal_coords : dict
        Dictionary representing the coordinates of each node.
        {node_id1 : [x1, y1],...}
    connectivity : dict
        Dictionary representing the 2 nodes associated with each element.
        {id : [nodei_id, nodej_id],...}
    force_vector : dict
        Dictionary representing the external force input onto the truss.
    boundary_conditions : dict
        Dictionary representing the boundary condition constraints.
    K : ndarray
        Stiffness matrix for the truss.
    nodes : dict
        A dictionary containing the nodes.
    elements : dict
        A dictionary containing the elements.
    disp_vector : dict
        Dictionary representing the displacement of each node.
    stress: dict
        Dictionary representing the stresses in the truss.

    Methods
    -------
    create_nodes()
    create_elements()
    assemblage()
    displacement()
    stress()

    """

    def __init__(
        self,
        mat_prop,
        nodal_coords,
        connectivity,
        force_vector,
        boundary_conditions
    ):
        self.E = mat_prop['E']
        self.A = mat_prop['A']
        self.nodal_coords = nodal_coords
        self.connectivity = connectivity
        self.force_vector = force_vector
        self.boundary_conditions = boundary_conditions
        self.K = np.zeros([])
        self.nodes = {}
        self.elements = {}
        self.disp_vector = {}
        self.stress = {}

    def create_nodes():
        pass

    def create_elements():
        pass

    def assemblage():
        pass

    def displacement():
        pass

    def stress():
        pass
