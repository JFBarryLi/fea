'''
Finite Element Analysis for 2D frame or Truss
Author : Barry Li
Licence : MIT 
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
	
	'''
	
	def __init__(self, nodei, nodej, E, ID, OD):
		self.nodei = nodei
		self.nodej = nodej
		self.E = E
		self.ID = ID
		self.OD = OD
		
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
	connectivity_table : dict
		Dictionary representing the 2 nodes associated with each element {element_id : [nodei_id, nodej_id],...}
	nodal_coordinates : dict
		Dictionary representing the coordinates of each node {node_id1 : [x1, y1],...}
	boundary_conditions : list
		List representing the boundary conditions [0,15,22,...]
		Each node has 3 degrees of freedom, the list determines which DOF are fixed
		1 correspond to node_1 x-direction, 2 correspond to node_1 y-direction, 3 correspond to node_1 theta, 4 correspond to node_2 x-direction ...
	force_vector : list
		List representing the input force into the structure [fx1, fy1, theta1, ...]
	'''
	
	@abstractmethod
	def __init__(self, outer_diameter, inner_diameter, modulus_elasticity,
				 connectivity_table, nodal_coordinates,
				 boundary_conditions, force_vector):
				 
		self.outer_diameter = outer_diameter
		self.inner_diameter = inner_diameter
		self.modulus_elasticity = modulus_elasticity
		self.connectivity_table = connectivity_table
		self.nodal_coordinates = nodal_coordinates
		self.boundary_conditions = boundary_conditions
		self.force_vector = force_vector
		self.nodes = {}
		self.elements = {}
		self.stress = {}
		self.new_nodal_coordinates = {}
	
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
						  self.inner_diameter, self.outer_diameter)
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
		
		zero_force_rows = []
		# Remove rows cooresponding to force=0
		for i in range(0, len(self.force_vector)):
			if self.force_vector[i] == 0:
				zero_force_rows.append(i)	
		
		# Add zero_force_rows to boundary condition indices
		bc = self.boundary_conditions + zero_force_rows
		bc = list(set(bc))
		
		# Remove degree of freedom corresponding to the boundary_conditions
		force_bc_removed = np.delete(self.force_vector, bc, axis=0)
		force_bc_removed = np.matrix(force_bc_removed).transpose()
		assemblage_bc_removed = np.delete(self.assemblage, bc, axis=0)
		assemblage_bc_removed = np.delete(assemblage_bc_removed, bc, axis=1)
		
		# Displacement = Assemblage Matrix divided by Force vector
		self.Q = np.linalg.inv(assemblage_bc_removed) * force_bc_removed
		
		# Insert zero rows into the displacement vector at the locaiton of the boundary conditions
		total_dof_index = np.linspace(0, size - 1, num = size, dtype = int)
		dof_index_without_bc = np.setdiff1d(total_dof_index, bc)
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
		for i in range(1, int(len(nodal_coordinates_list)/2+1)):
			self.new_nodal_coordinates[i] = [nodal_coordinates_list[2*i-2], nodal_coordinates_list[2*i-1]]
		
	def calc_stress(self):
		'''
		Calculate stress in each member
		'''
	
		for i in range(1, int(len(self.elements) + 1)):
			
			ele = self.elements[i]
			# Displacements in Global Coordinates
			qix = self.Q[ele.nodei.id * 3 - 3]
			qiy = self.Q[ele.nodei.id * 3 - 2]
			qjx = self.Q[ele.nodej.id * 3 - 3]
			qjy = self.Q[ele.nodej.id * 3 - 2]
			
			
			# Displacements in Local Coordinates
			qix_local = qix * ele.Cx + qiy * ele.Cy
			qjx_local = qjx * ele.Cx + qjy * ele.Cy
			
			qiy_local = qix * -ele.Cy + qiy * ele.Cx
			qjy_local = qjx * -ele.Cy + qjy * ele.Cx
			qi_theta = self.Q[ele.nodei.id * 3 - 1]
			qj_theta = self.Q[ele.nodej.id * 3 - 1]
			
			# Axial stress
			axial_stress = self.modulus_elasticity * (qjx_local - qix_local) / ele.L
		
			# Bending stress
			bending_stress_i = self.modulus_elasticity * self.outer_diameter/2 * ((6/ele.L*(qiy_local-qjy_local))+(2/ele.L*(2*qi_theta+qj_theta)))
			bending_stress_j = self.modulus_elasticity * self.outer_diameter/2 * ((6/ele.L*(qiy_local-qjy_local))+(2/ele.L*(2*qj_theta+qi_theta)))
			bending_stress = np.max([bending_stress_i, bending_stress_j])
			
			# Shear stress
			shear_stress = self.modulus_elasticity * ele.I * ((12/ele.L**3)*(qiy_local-qjy_local)+(6/ele.L**2)*(qi_theta+qj_theta))
			
			# Principal stress
			principal_stress_1 = (axial_stress + bending_stress)/2 + np.sqrt(((axial_stress-bending_stress)/2)**2+shear_stress**2)
			principal_stress_2 = (axial_stress + bending_stress)/2 - np.sqrt(((axial_stress-bending_stress)/2)**2+shear_stress**2)
			max_stress = np.max([principal_stress_1, principal_stress_2])
			min_stress = np.min([principal_stress_1, principal_stress_2])
			
			# Von Mises stress
			von_mises_stress = np.sqrt(max_stress**2-max_stress*min_stress+min_stress**2)
			
			self.stress[i] = [von_mises_stress]
	
		pass

	
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
			nodal_coordinates_list[i] = nodal_coordinates_list[i] + self.Q[i] 

		# Constructing the new_nodal_coordinates dictionary
		for i in range(1, int(len(nodal_coordinates_list)/2+1)):
			self.new_nodal_coordinates[i] = [nodal_coordinates_list[2*i-2], nodal_coordinates_list[2*i-1]]
	
	def calc_stress(self):
		'''
		Calculate stress in each member
		'''
	
		for i in range(1, int(len(self.elements) + 1)):
			
			ele = self.elements[i]
			# Displacements in Global Coordinates
			qix = self.Q[ele.nodei.id * 2 - 2]
			qiy = self.Q[ele.nodei.id * 2 - 1]
			qjx = self.Q[ele.nodej.id * 2 - 2]
			qjy = self.Q[ele.nodej.id * 2 - 1]
			
			# Displacements in Local Coordinates
			qi_local = qix * ele.Cx + qiy * ele.Cy
			qj_local = qjx * ele.Cx + qjy * ele.Cy
			self.stress[i] = self.modulus_elasticity * (qj_local - qi_local) / ele.L
	
class fea():
	'''
	FEA class, perform fea analysis on the structure
	
	Parameters
	----------
	outer_diameter : float [mm]
	inner_diameter : float [mm]
	modulus_elasticity : float [MPa]
	connectivity_table : dict
		Dictionary representing the 2 nodes associated with each element {element_id : [nodei_id, nodej_id],...}
	nodal_coordinates : dict
		Dictionary representing the coordinates of each node {node_id1 : [x1, y1],...}
	boundary_conditions : list
		List representing the boundary conditions [0,15,22,...]
		Each node has 3 degrees of freedom, the list determines which DOF are fixed
		1 correspond to node_1 x-direction, 2 correspond to node_1 y-direction, 3 correspond to node_1 theta, 4 correspond to node_2 x-direction ...
	force_vector : list
		List representing the input force into the structure [fx1, fy1, theta1, ...]
	frame_or_truss : char
		Specify which type of structure to create
	'''
	
	def __init__(self, outer_diameter, inner_diameter, modulus_elasticity,
				 connectivity_table, nodal_coordinates,
				 boundary_conditions, force_vector, frame_or_truss):
				 
		self.outer_diameter = outer_diameter
		self.inner_diameter = inner_diameter
		self.modulus_elasticity = modulus_elasticity
		self.connectivity_table = connectivity_table
		self.nodal_coordinates = nodal_coordinates
		self.boundary_conditions = boundary_conditions
		self.force_vector = force_vector
		self.frame_or_truss = frame_or_truss
	
	def data_validate(self):
		'''
		Validate the input data and return common errors
		'''
	
		if self.inner_diameter >= self.outer_diameter:
			return "ERROR: inner diameter greater or equal to outer diameter"
		elif self.frame_or_truss != 'frame' and self.frame_or_truss != 'truss':
			return "ERROR: must specify either frame or truss"
		elif len(self.boundary_conditions) > len(self.nodal_coordinates)*2 and self.frame_or_truss == 'truss':
			return "ERROR: too many boundary conditions, maximum: 2*(# of nodes)"
		elif len(self.boundary_conditions) > len(self.nodal_coordinates)*3 and self.frame_or_truss == 'frame':
			return "ERROR: too many boundary conditions, maximum: 3*(# of nodes)"
		elif len(self.force_vector) < len(self.nodal_coordinates)*2 and self.frame_or_truss == 'truss':
			return "ERROR: size of force vector vector too small, require 2*(# of nodes)"
		elif len(self.force_vector) < len(self.nodal_coordinates)*3 and self.frame_or_truss == 'frame':
			return "ERROR: size of force vector too small, require 3*(# of nodes)"
		else:
			return True
	
	def analyze(self):
		'''
		Call all relevant methods to calculate stress
		'''
		
		if self.data_validate() != True:
			return self.data_validate()
		
		if self.frame_or_truss == 'frame':
			self.struc = frame(self.outer_diameter, self.inner_diameter, self.modulus_elasticity,
							   self.connectivity_table, self.nodal_coordinates,
							   self.boundary_conditions, self.force_vector)
		elif self.frame_or_truss == 'truss':
			self.struc = truss(self.outer_diameter, self.inner_diameter, self.modulus_elasticity,
							   self.connectivity_table, self.nodal_coordinates,
							   self.boundary_conditions, self.force_vector)
							   
		self.struc.create_nodes()
		self.struc.create_elements()
		self.struc.calc_properties()
		self.struc.calc_stiffness()
		self.struc.calc_assemblage()
		self.struc.calc_displacement()
		self.struc.calc_new_nodal_coordinates()
		self.struc.calc_stress()
		
		self.new_nodal_coordinates = self.struc.new_nodal_coordinates
		self.stress = self.struc.stress
		
		return 'success'