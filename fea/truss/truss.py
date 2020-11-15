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
        {'ele_id' : {'index': ..., 'E': ..., 'A': ...}, ...}
    nodal_coords : dict
        Dictionary representing the coordinates of each node.
        {'node_id': {'index': ..., 'x': ..., 'y': ..., 'z': ...}, ...}
    deformed_nodal_coords : dict
        Dictionary representing the deformed coordinates of each node.
        {'node_id': {'index': ..., 'x': ..., 'y': ..., 'z': ...}, ...}
    connectivity : dict
        Dictionary representing the 2 nodes associated with each element.
        {'ele_id' : {'index': ..., 'i': 'nodei_id', 'j': 'nodej_id'}, ...}
    force_vector : dict
        Dictionary representing the external force input onto the truss.
        {'node_id': {
            'index': ...,
            'u1': {'index': ..., 'value': ...},
            'u2': {'index': ..., 'value': ...},
            'u3': {'index': ..., 'value': ...},
        }, ...}
    boundary_conditions : dict
        Dictionary representing the boundary condition constraints.
        {'node_id': {
            'index': ...,
            'u1': {'index': ..., 'value': ...},
            'u2': {'index': ..., 'value': ...},
            'u3': {'index': ..., 'value': ...},
        }, ...}
    K : ndarray
        Stiffness matrix for the truss.
    Q : ndarray
        Displacement matrix for the truss.
    nodes : dict
        A dictionary containing the nodes.
    elements : dict
        A dictionary containing the elements.
    stresses: dict
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
        # A truss structure have 3 degrees of freedom.
        self.DOF = 3
        self.mat_prop = mat_prop
        self.nodal_coords = nodal_coords
        self.deformed_nodal_coords = nodal_coords
        self.connectivity = connectivity
        self.force_vector = force_vector
        self.boundary_conditions = boundary_conditions
        self.K = np.zeros([])
        self.Q = np.zeros([])
        self.nodes = {}
        self.elements = {}
        self.disp_vector = {}
        self.stresses = {}

    def create_nodes(self):
        log.info('Instantiating truss nodes.')
        for node in self.nodal_coords:
            self.nodes[node] = Node(
                node,
                self.nodal_coords[node]['index'],
                self.nodal_coords[node]['x'],
                self.nodal_coords[node]['y'],
                self.nodal_coords[node]['z']
            )

    def create_elements(self):
        log.info('Instantiating truss elements.')
        for ele in self.connectivity:
            self.elements[ele] = Element(
                ele,
                self.connectivity[ele]['index'],
                self.nodes[self.connectivity[ele]['i']],
                self.nodes[self.connectivity[ele]['j']],
                self.mat_prop[ele]
            )
            self.elements[ele].stiffness()

    def assemblage(self):
        log.info('Calculating assemblage stiffness matrix.')
        DOF = self.DOF
        size = len(self.nodes) * DOF

        # Initialize assemblage matrix to zeros
        assemblage = np.zeros([size, size])

        # Add each element's stiffness matrix to the assemblage matrix
        for ele in self.elements.values():
            nodei_index = ele.nodei.index
            nodej_index = ele.nodej.index

            # Quadrant 1
            # row: [ix, iy, iz], col: [ix, iy, iz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodei_index + j,
                        DOF*nodei_index + k
                    ] = assemblage[
                        DOF*nodei_index + j,
                        DOF*nodei_index + k
                    ] + ele.K[j, k]

            # Quadrant 2
            # row:[ix, iy, iz], col:[jx, jy, jz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodei_index + j,
                        DOF*nodej_index + k
                    ] = assemblage[
                        DOF*nodei_index + j,
                        DOF*nodej_index + k
                    ] + ele.K[j, k + DOF]

            # Quadrant 3
            # row:[jx, jy, jz], col:[ix, iy, iz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodej_index + j,
                        DOF*nodei_index + k
                    ] = assemblage[
                        DOF*nodej_index + j,
                        DOF*nodei_index + k
                    ] + ele.K[j + DOF, k]

            # Quadrant 4
            # row:[jx, jy, jz], col:[jx, jy, jz]
            for j in range(0, DOF):
                for k in range(0, DOF):
                    assemblage[
                        DOF*nodej_index + j,
                        DOF*nodej_index + k
                    ] = assemblage[
                        DOF*nodej_index + j,
                        DOF*nodej_index + k
                    ] + ele.K[j + DOF, k + DOF]

        log.info('Finished calculating assemblage stiffness matrix.')
        self.K = assemblage

    def displacement(self):
        log.info('Calculating displacement of each node.')
        DOF = self.DOF
        size = len(self.nodes) * DOF

        # Find indices to remove from the assemblage matrix
        log.info('Reducing the matrices based on the boundary conditions.')
        constraints = []
        for node in self.boundary_conditions:
            node_index = self.boundary_conditions[node]['index']
            for freedom in self.boundary_conditions[node]:
                if freedom == 'index':
                    continue
                freedom_index = self.boundary_conditions[node][freedom]['index']
                if self.boundary_conditions[node][freedom]['value'] == 0:
                    constraints.append(DOF*node_index + freedom_index)

        # Constructing the force matrix
        log.info('Constructing the force matrix.')
        forces = np.zeros([size, 1])
        for node in self.force_vector:
            node_index = self.boundary_conditions[node]['index']
            for freedom in self.force_vector[node]:
                if freedom == 'index':
                    continue
                freedom_index = self.force_vector[node][freedom]['index']
                forces[
                    DOF*node_index + freedom_index
                ] = self.force_vector[node][freedom]['value']

        K_reduced = np.delete(self.K, constraints, axis=0)
        K_reduced = np.delete(K_reduced, constraints, axis=1)
        forces_reduced = np.delete(forces, constraints, axis=0)

        # Solve the reduced linear system
        log.info('Solving the linear system.')
        Q_zero = np.zeros([size, 1])
        Q = np.linalg.solve(K_reduced, forces_reduced)

        # Reconstruct displacement vector back to original size
        log.info('Reconstructing the displacement vector.')
        total_dof_index = np.linspace(
            0,
            size - 1,
            num=size,
            dtype=int
        )
        dof_index_without_constraints = np.setdiff1d(
            total_dof_index,
            constraints
        )

        for i in range(0, len(Q)):
            Q_zero[dof_index_without_constraints[i]] = Q[i]

        self.Q = Q_zero

    def stress(self):
        DOF = self.DOF
        log.info('Computing axial stress for each element.')
        for e in self.elements:
            ele = self.elements[e]

            # Displacements in Global Coordinates
            qix = self.Q[ele.nodei.index*DOF + 0][0]
            qiy = self.Q[ele.nodei.index*DOF + 1][0]
            qiz = self.Q[ele.nodei.index*DOF + 2][0]
            qjx = self.Q[ele.nodej.index*DOF + 0][0]
            qjy = self.Q[ele.nodej.index*DOF + 1][0]
            qjz = self.Q[ele.nodej.index*DOF + 2][0]

            # Displacements in Local Coordinates
            qi_local = qix*ele.Cx + qiy*ele.Cy + qiz*ele.Cz
            qj_local = qjx*ele.Cx + qjy*ele.Cy + qjz*ele.Cz

            # Local element stress
            self.stresses[e] = ele.E * (qj_local - qi_local) / ele.L

    def calculate_deformed_nodal_coords(self):
        DOF = self.DOF
        log.info('Calculating the deformed nodal coordinates.')
        for q in range(0, int(len(self.Q) / DOF)):
            qx = self.Q[q*DOF + 0][0]
            qy = self.Q[q*DOF + 1][0]
            qz = self.Q[q*DOF + 2][0]

            node_id_map = {
                self.deformed_nodal_coords[id]['index']:
                    id for id in self.deformed_nodal_coords
            }

            node_id = node_id_map[q]
            self.deformed_nodal_coords[node_id]['x'] += qx
            self.deformed_nodal_coords[node_id]['y'] += qy
            self.deformed_nodal_coords[node_id]['z'] += qz
