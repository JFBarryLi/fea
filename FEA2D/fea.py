'''
Finite Element Analysis for 2D frame or Truss
'''

import numpy as np

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
		