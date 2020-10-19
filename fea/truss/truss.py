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
        {node_id: {x: ..., y: ..., z: ...}, ...}
    connectivity : dict
        Dictionary representing the 2 nodes associated with each element.
        {ele_id : {i: nodei_id, j: nodej_id}, ...}
    force_vector : dict
        Dictionary representing the external force input onto the truss.
        {node_id: {x: ..., y:..., z: ...}, ...}
    boundary_conditions : dict
        Dictionary representing the boundary condition constraints.
        {node_id: {x: ..., y:..., z: ...}, ...}
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
        log.info('Initializing truss solver.')
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

    def create_nodes(self):
        log.info('Instantiating truss nodes.')
        for node in self.nodal_coords:
            self.nodes[node] = Node(
                node,
                self.nodal_coords[node]['x'],
                self.nodal_coords[node]['y'],
                self.nodal_coords[node]['z']
            )

    def create_elements(self):
        log.info('Instantiating truss elements.')
        for ele in self.connectivity:
            self.elements[ele] = Element(
                ele,
                self.nodes[self.connectivity[ele]['i']],
                self.nodes[self.connectivity[ele]['j']],
                self.E,
                self.A
            )
            self.elements[ele].stiffness()

    def assemblage(self):
        log.info('Calculating assemblage stiffness matrix.')
        # A truss structure have 3 degrees of freedom.
        DOF = 3
        size = len(self.nodes) * DOF

        # Initialize assemblage matrix to zeros
        assemblage = np.zeros([size, size])

        # Add each element's stiffness matrix to the assemblage matrix
        for ele in self.elements.values():
            nodei_id = ele.nodei.id
            nodej_id = ele.nodej.id

            # Quadrant 1
            # row: [ix, iy, iz], col: [ix, iy, iz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodei_id - DOF + j,
                        DOF*nodei_id - DOF + k
                    ] = assemblage[
                        DOF*nodei_id - DOF + j,
                        DOF*nodei_id - DOF + k
                    ] + ele.K[j, k]

            # Quadrant 2
            # row:[ix, iy, iz], col:[jx, jy, jz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodei_id - DOF + j,
                        DOF*nodej_id - DOF + k
                    ] = assemblage[
                        DOF*nodei_id - DOF + j,
                        DOF*nodej_id - DOF + k
                    ] + ele.K[j, k + DOF]

            # Quadrant 3
            # row:[jx, jy, jz], col:[ix, iy, iz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodej_id - DOF + j,
                        DOF*nodei_id - DOF + k
                    ] = assemblage[
                        DOF*nodej_id - DOF + j,
                        DOF*nodei_id - DOF + k
                    ] + ele.K[j + DOF, k]

            # Quadrant 4
            # row:[jx, jy, jz], col:[jx, jy, jz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodej_id - DOF + j,
                        DOF*nodej_id - DOF + k
                    ] = assemblage[
                        DOF*nodej_id - DOF + j,
                        DOF*nodej_id - DOF + k
                    ] + ele.K[j + DOF, k + DOF]

        log.info('Finished calculating assemblage stiffness matrix.')
        self.K = assemblage

    def displacement():
        pass

    def stress():
        pass
