'''
Finite Element Analysis for 2D frame or Truss
'''

import numpy as np

class frame():
	'''
	Frame class, represent the frame structure that is made up of nodes and elements
	
	Parameters
	----------
	outer_diameter : float [mm]
	inner_diameter : float [mm]
	modulus_elasticity : float [MPa]
	yield_strength : float [MPa]
	connectivity_table : dict
		Dictionary representing the 2 nodes associated with each element {element_id : [nodei_id, nodej_id],...}
	nodal_coordinates : dict
		Dictionary representing the coordinates of each node {node_id1 : [x1, y1],...}
	boundary_conditions : array
		Array representing the boundary conditions [0,15,22,...]
		Each node has 3 degrees of freedom, the array determines which DOF are fixed
		1 correspond to node_1 x-direction, 2 correspond to node_1 y-direction, 3 correspond to node_1 theta, 4 correspond to node_1 x-direction ...
	force_vector : array
		Array representing the input force into the structure [fx1, fy1, theta1, ...]
	frame_or_truss : char 
		'frame' or 'truss', determine how the assemblage matrix is calculated
	'''
	
	def __init__(self, outer_diameter, inner_diameter, modulus_elasticity,
				 yield_strength, connectivity_table, nodal_coordinates,
				 boundary_conditions, force_vector, frame_or_truss):
				 
		self.outer_diameter = outer_diameter
		self.inner_diameter = inner_diameter
		self.modulus_elasticity = modulus_elasticity
		self.yield_strength = yield_strength
		self.connectivity_table = connectivity_table
		self.nodal_coordinates = nodal_coordinates
		self.boundary_conditions = boundary_conditions
		self.force_vector = force_vector
		self.frame_or_truss = frame_or_truss
		self.nodes = {}
		self.elements = {}
	
	def create_nodes(self):
		'''
		Create the node objects according to the nodal_coordinates
		'''
		
		for key in self.nodal_coordinates:
			n = node(key, self.nodal_coordinates[key][0], self.nodal_coordinates[key][1])
			self.nodes[n.id] = n
		
	def create_elements(self):
		'''
		Create element objects according to connectivity_table
		'''
		
		for key in self.connectivity_table:
			# Retrieve node from nodes
			nodei = self.nodes[self.connectivity_table[key][0]]
			nodej = self.nodes[self.connectivity_table[key][1]]
			
			# Instantiate an element
			ele = element(nodei, nodej, self.modulus_elasticity, 
						  self.inner_diameter, self.outer_diameter, 
						  self.yield_strength, self.frame_or_truss)
			ele.id = key
			self.elements[ele.id] = ele
			
	def calc_properties(self):
		'''
		Calculate the geometric properties of each element
		'''
	
		for ele in self.elements.values():
			ele.calc_properties()
			
	def calc_stiffness(self):
		'''
		Calculate the stiffness matrix for each element
		'''
		
		for ele in self.elements.values():
			ele.calc_stiffness()
		
	def calc_assemblage(self):
		'''
		Calculate the assemblage matrix for the frame
		'''
		
		if self.frame_or_truss == 'frame':
			# Degrees of freedom per node
			DOF = 3
		elif self.frame_or_truss == 'truss':
			DOF = 2
		
		size = len(self.nodes) * DOF
		
		# Initialize assemblage matrix to zeros
		self.assemblage = np.zeros([size, size])
		
		# Add each element's stiffness matrix to the assemblage matrix
		for ele in self.elements.values():
			nodei_id = ele.nodei.id
			nodej_id = ele.nodej.id
			
			# Quadrant 1 
			# for frame; row:[ix,iy,itheta] col:[ix,iy,itheta]
			# for truss; row:[ix,iy] col:[ix,iy]
			for j in range(0,DOF):
				for k in range(0,DOF):
					self.assemblage[DOF*nodei_id - DOF + j, DOF*nodei_id - DOF + k] = \
					self.assemblage[DOF*nodei_id - DOF + j, DOF*nodei_id - DOF + k] + \
					ele.K[j,k]

			# Quadrant 2 
			# for frame; row:[ix,iy,itheta] col:[jx,jy,jz,jtheta]
			# for truss; row:[ix,iy,itheta] col:[jx,jy,jz,jtheta]
			for j in range(0,DOF):
				for k in range(0,DOF):
					self.assemblage[DOF*nodei_id - DOF + j, DOF*nodej_id - DOF + k] = \
					self.assemblage[DOF*nodei_id - DOF + j, DOF*nodej_id - DOF + k] + \
					ele.K[j,k+DOF]

			# Quadrant 3 
			# for frame; row:[jx,jy,jz,itheta] col:[ix,iy,jtheta]
			# for truss; row:[jx,jy,jz,itheta] col:[ix,iy,jtheta]
			for j in range(0,DOF):
				for k in range(0,DOF):
					self.assemblage[DOF*nodej_id - DOF + j, DOF*nodei_id - DOF + k] = \
					self.assemblage[DOF*nodej_id - DOF + j, DOF*nodei_id - DOF + k] + \
					ele.K[j+DOF,k]
					
			# Quadrant 4 
			# for frame; row:[jx,jy,jz,itheta] col:[jx,jy,jz,jtheta]
			# for truss; row:[jx,jy,jz,itheta] col:[jx,jy,jz,jtheta]
			for j in range(0,DOF):
				for k in range(0,DOF):
					self.assemblage[DOF*nodej_id - DOF + j, DOF*nodej_id - DOF + k] = \
					self.assemblage[DOF*nodej_id - DOF + j, DOF*nodej_id - DOF + k] + \
					ele.K[j+DOF,k+DOF]
						
	def calc_displacement(self):
		'''
		Calculate the displacement vector for each element
		'''
		if self.frame_or_truss == 'frame':
			# Degrees of freedom per node
			DOF = 3
		elif self.frame_or_truss == 'truss':
			DOF = 2
		
		size = len(self.nodes) * DOF
		
		# Remove degree of freedom corresponding to the boundary_conditions
		force_bc_removed = np.delete(self.force_vector, self.boundary_conditions, axis=0)
		force_bc_removed = np.matrix(force_bc_removed).transpose()
		assemblage_bc_removed = np.delete(self.assemblage, self.boundary_conditions, axis=0)
		assemblage_bc_removed = np.delete(assemblage_bc_removed, self.boundary_conditions, axis=1)
			
		# Displacement = Assemblage Matrix divided by Force vector
		self.Q = np.linalg.inv(assemblage_bc_removed) * force_bc_removed
		
		# Insert zero rows into the displacement vector at the locaiton of the boundary conditions
		total_dof_index = np.linspace(0, size - 1, num = size, dtype = int)
		dof_index_without_bc = np.setdiff1d(total_dof_index, self.boundary_conditions)
		zero_Q = np.zeros([size,1])
		
		for i in range(0,len(self.Q)):
			zero_Q[dof_index_without_bc[i]] = self.Q[i] 
		
		self.Q = zero_Q
		
class element():
	'''
	Element class, represent a bar element with circular/tubular cross section
	
	Parameters
	----------
	nodei : obj 
		Node object, representing node i
	nodej : obj
		Node object, representing node j
	E : float [MPa]
		Young's Modulus
	ID : float [mm]
		Inner Diameter
	OD : float [mm]
		Outer Diameter
	Sy : float [MPa]
		Yield Strength
	frame_or_truss : char
		'frame' or 'truss', determine how the assemblage matrix is calculated
	
	'''
	
	def __init__(self, nodei, nodej, E, ID, OD, Sy, frame_or_truss):
		self.nodei = nodei
		self.nodej = nodej
		self.E = E
		self.ID = ID
		self.OD = OD
		self.Sy = Sy
		self.frame_or_truss = frame_or_truss
		
	def calc_properties(self):
		'''
		Calculates properties of the element
		'''
		
		# Length [mm]
		self.L = np.sqrt((self.nodej.x - self.nodei.x)**2 + 
						 (self.nodej.y - self.nodei.y)**2)
		
		#Cosinex 
		self.Cx = (self.nodej.x - self.nodei.x) / self.L
		
		#Cosiney
		self.Cy = (self.nodej.y - self.nodei.y) / self.L
		
		#Moment of Inertia [mm^4]
		self.I = (self.OD**4 - self.ID**4) * np.pi / 64
		
		#Cross Sectional Area [mm^2]
		self.A = (self.OD**2 - self.ID**2) * np.pi / 4
		
	def calc_stiffness(self):
		'''
		Calculate the stiffness matrix 
		'''
		
		if self.frame_or_truss == 'frame':
            # Local Stiffness Matrix
			self.k_local = np.matrix([[self.A*self.E/self.L, 0, 0, -self.A*self.E/self.L, 0, 0],
									  [0, 12*self.E*self.I/self.L**3, 6*self.E*self.I/self.L**2, 0, -12*self.E*self.I/self.L**3, 6*self.E*self.I/self.L**2],
									  [0, 6*self.E*self.I/self.L**2, 4*self.E*self.I/self.L, 0, -6*self.E*self.I/self.L**2, 2*self.E*self.I/self.L],
									  [-self.A*self.E/self.L, 0, 0, self.A*self.E/self.L, 0, 0],
									  [0, -12*self.E*self.I/self.L**3, -6*self.E*self.I/self.L**2, 0, 12*self.E*self.I/self.L**3, -6*self.E*self.I/self.L**2],
									  [0, 6*self.E*self.I/self.L**2, 2*self.E*self.I/self.L, 0, -6*self.E*self.I/self.L**2, 4*self.E*self.I/self.L]])
            
            # Local to Global Coordinate Transformation Matrix
			self.R = np.matrix([[self.Cx, -self.Cy, 0, 0, 0, 0],
								[self.Cy, self.Cx, 0, 0, 0, 0],
								[0, 0, 1, 0, 0, 0],
								[0, 0, 0, self.Cx, -self.Cy, 0],
								[0, 0, 0, self.Cy, self.Cx, 0],
								[0, 0, 0, 0, 0, 1]])
            
            # Global Stiffness Matrix
			self.K = self.R.transpose() * self.k_local * self.R;
			
		elif self.frame_or_truss == 'truss':
			# Global Stiffness Matrix
			self.K = self.E*self.A/self.L * np.matrix([[self.Cx**2, self.Cx*self.Cy, -self.Cx**2, -self.Cx*self.Cy],
													   [self.Cx*self.Cy, self.Cy**2, -self.Cx*self.Cy, -self.Cy**2],
													   [-self.Cx**2, -self.Cx*self.Cy, self.Cx**2, self.Cx*self.Cy],
													   [-self.Cx*self.Cy, -self.Cy**2, self.Cx*self.Cy, self.Cy**2]])
		
class node():
	'''
	Node class, represent a point of the structure
	
	Parameters
	----------
	id : int
	x : float
	y : float
	
	'''

	def __init__(self, id, x, y):
		self.id = id
		self.x = x
		self.y = y