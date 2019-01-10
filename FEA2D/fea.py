'''
Finite Element Analysis for 2D frame or Truss
'''

import numpy as np
from abc import ABC, abstractmethod

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
	
	'''
	
	def __init__(self, nodei, nodej, E, ID, OD, Sy):
		self.nodei = nodei
		self.nodej = nodej
		self.E = E
		self.ID = ID
		self.OD = OD
		self.Sy = Sy
		
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
		
	def calc_stiffness_frame(self):
		'''
		Calculate the stiffness matrix for a frame
		'''
		
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


		
	def calc_stiffness_truss(self):
		# Global Stiffness Matrix
		self.K = self.E*self.A/self.L * np.matrix([[self.Cx**2, self.Cx*self.Cy, -self.Cx**2, -self.Cx*self.Cy],
												   [self.Cx*self.Cy, self.Cy**2, -self.Cx*self.Cy, -self.Cy**2],
												   [-self.Cx**2, -self.Cx*self.Cy, self.Cx**2, self.Cx*self.Cy],
												   [-self.Cx*self.Cy, -self.Cy**2, self.Cx*self.Cy, self.Cy**2]])
	
class structure(ABC):
	'''
	Abstract base class, basic structure class. Parent class to frame and truss
	
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
	'''
	
	@abstractmethod
	def __init__(self, outer_diameter, inner_diameter, modulus_elasticity,
				 yield_strength, connectivity_table, nodal_coordinates,
				 boundary_conditions, force_vector):
				 
		self.outer_diameter = outer_diameter
		self.inner_diameter = inner_diameter
		self.modulus_elasticity = modulus_elasticity
		self.yield_strength = yield_strength
		self.connectivity_table = connectivity_table
		self.nodal_coordinates = nodal_coordinates
		self.boundary_conditions = boundary_conditions
		self.force_vector = force_vector
		self.nodes = {}
		self.elements = {}
		self.stress = {}
	
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
						  self.yield_strength)
			ele.id = key
			self.elements[ele.id] = ele
			
	def calc_properties(self):
		'''
		Calculate the geometric properties of each element
		'''
	
		for ele in self.elements.values():
			ele.calc_properties()

	@abstractmethod
	def calc_stiffness(self):
		pass
	
	def calc_assemblage(self):
		'''
		Calculate the assemblage matrix for the frame
		'''
		
		DOF = self.DOF
		
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
		
		DOF = self.DOF
		
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
		
	@abstractmethod
	def calc_new_nodal_coordinates(self):
		pass
		
	@abstractmethod
	def calc_stress(self):
		pass
		
	@abstractmethod
	def calc_factor_of_safety(self):
		pass

class frame(structure):
	'''
	Frame class, represents the frame structure that is made up of nodes and elements
	'''
	
	def __init__(self, *args, **kwargs):
		super(frame, self).__init__(*args, **kwargs)
		self.DOF = 3
	
	def calc_stiffness(self):
		'''
		Calculate the stiffness matrix for each element
		'''
		
		for ele in self.elements.values():
			ele.calc_stiffness_frame()
			
	def calc_new_nodal_coordinates(self):
		'''
		Calculate the new nodal coordinates after the force vector is applied
		'''
		
		# Convert nodal coordinate dictionary to a list
		nodal_coordinates_list = []
		for key in sorted(self.nodal_coordinates.keys()):
			nodal_coordinates_list.append(self.nodal_coordinates[key][0])
			nodal_coordinates_list.append(self.nodal_coordinates[key][1])
			
		# Deleting every third row, the row that correspond with the rotating DOF
		disp_without_moment = np.delete(self.Q, self.Q[1::3]).transpose()
		
		for i in range(0, len(nodal_coordinates_list)):
			nodal_coordinates_list[i] = nodal_coordinates_list[i] + disp_without_moment[i] 

		# Constructing the new_nodal_coordinates dictionary
		self.new_nodal_coordinates = {}
		for i in range(1, int(len(nodal_coordinates_list)/2+1)):
			self.new_nodal_coordinates[i] = [nodal_coordinates_list[2*i-2], nodal_coordinates_list[2*i-1]]
		
	def calc_stress(self):
		'''
		Calculate stress in each member
		'''
	
		print('1')
		
	def calc_factor_of_safety(self):
		print('1')
	
class truss(structure):
	'''
	Truss class, represents the truss structure that is made up of nodes and elements
	'''
	
	def __init__(self, *args, **kwargs):
		super(truss, self).__init__(*args, **kwargs)
		self.DOF = 2

	def calc_stiffness(self):
		'''
		Calculate the stiffness matrix for each element
		'''
		
		for ele in self.elements.values():
			ele.calc_stiffness_truss()
	
	def calc_new_nodal_coordinates(self):
		'''
		Calculate the new nodal coordinates after the force vector is applied
		'''
		
		# Convert nodal coordinate dictionary to a list
		nodal_coordinates_list = []
		for key in sorted(self.nodal_coordinates.keys()):
			nodal_coordinates_list.append(self.nodal_coordinates[key][0])
			nodal_coordinates_list.append(self.nodal_coordinates[key][1])
			
		for i in range(0, len(nodal_coordinates_list)):
			nodal_coordinates_list[i] = nodal_coordinates_list[i] + disp_without_moment[i] 

		# Constructing the new_nodal_coordinates dictionary
		self.new_nodal_coordinates = {}
		for i in range(1, int(len(nodal_coordinates_list)/2+1)):
			self.new_nodal_coordinates[i] = [nodal_coordinates_list[2*i-2], nodal_coordinates_list[2*i-1]]
	
	def calc_stress(self):
		'''
		Calculate stress in each member
		'''
	
		for i in range(1, int(len(self.elements) + 1)):
			
			ele = self.elements[i]
			# Displacements in Global Coordinates
			qxi = self.Q[ele.nodei.id * 2 - 2]
			qyi = self.Q[ele.nodei.id * 2 - 1]
			qxj = self.Q[ele.nodej.id * 2 - 2]
			qyj = self.Q[ele.nodej.id * 2 - 1]
			
			# Displacements in Local Coordinates
		
			qi_local = qxi * ele.Cx + qyi * ele.Cy
			qj_local = qxj * ele.Cx + qyj * ele.Cy
			self.stress[i] = self.modulus_elasticity * (qj_local - qi_local) / self.elements[i].L
	
		
	def calc_factor_of_safety(self):
		print('1')
		

