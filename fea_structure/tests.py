from django.test import TestCase

from .models import InputStructure, OutputStructure, InputOutputLink
from .serializers import InputStructureSerializer, OutputStructureSerializer
from .views import fea_structure_input, fea_structure_output

from rest_framework.test import APIRequestFactory

from .fea import node, element, structure, frame, truss, fea

import numpy as np
	
class InputStructureModelTests(TestCase):

	def test_object_creation_with_normal_values(self):
		'''
		Check that InputStructure objects are created and saved properly
		'''
		struc = InputStructure(moment_of_inertia_y=99.99,
							   moment_of_inertia_z=99.99,
							   cross_sectional_area=99.99,
							   y_max=99.99,
							   young_modulus=99.99,
							   shear_modulus=99.99,
							   torsional_constant=99.99,
							   connectivity_table='testct',
							   nodal_coordinates='testnc',
							   boundary_conditions='testbc',
							   frame_or_truss='tesft')
		
		self.assertEqual(struc.moment_of_inertia_y, 99.99)
		self.assertEqual(struc.moment_of_inertia_z, 99.99)
		self.assertEqual(struc.cross_sectional_area, 99.99)
		self.assertEqual(struc.y_max, 99.99)
		self.assertEqual(struc.young_modulus, 99.99)
		self.assertEqual(struc.shear_modulus, 99.99)
		self.assertEqual(struc.torsional_constant, 99.99)
		self.assertEqual(struc.connectivity_table, 'testct')
		self.assertEqual(struc.nodal_coordinates, 'testnc')
		self.assertEqual(struc.boundary_conditions, 'testbc')
		self.assertEqual(struc.frame_or_truss, 'tesft')
	
	def test_object_save(self):
		'''
		Check InputStructure are saved properly
		'''
		struc = InputStructure(moment_of_inertia_y=99.99,
							   moment_of_inertia_z=99.99,
							   cross_sectional_area=99.99,
							   y_max=99.99,
							   young_modulus=99.99,
							   shear_modulus=99.99,
							   torsional_constant=99.99,
							   connectivity_table='testct',
							   nodal_coordinates='testnc',
							   boundary_conditions='testbc',
							   frame_or_truss='tesft')
		struc.save()
		
		self.assertEqual(InputStructure.objects.order_by('created')[0].nodal_coordinates, 'testnc')
	
class OutputStructureModelTests(TestCase):
	def test_object_creation_with_normal_values(self):
		'''
		Check that OutputStructure objects are created properly
		'''
		struc = OutputStructure(nodal_coordinates='test123', stress='test123')
		
		self.assertEqual(struc.nodal_coordinates, 'test123')
		self.assertEqual(struc.stress, 'test123')
	
	def test_object_save(self):
		'''
		Check OutputStructure are saved properly
		'''
		struc = OutputStructure(nodal_coordinates='test123', stress='test123')
		struc.save()
		
		self.assertEqual(OutputStructure.objects.order_by('created')[0].nodal_coordinates, 'test123')
		self.assertEqual(OutputStructure.objects.order_by('created')[0].stress, 'test123')
		
class InputStructureSerializerTests(TestCase):
	def test_serializer_with_normal_data(self):
		'''
		Check serializer output with normal data
		'''
		struc = InputStructure(moment_of_inertia_y=99.99,
							   moment_of_inertia_z=99.99,
							   cross_sectional_area=99.99,
							   y_max=99.99,
							   young_modulus=99.99,
							   shear_modulus=99.99,
							   torsional_constant=99.99,
							   connectivity_table='testct',
							   nodal_coordinates='testnc',
							   boundary_conditions='testbc',
							   force_vector='testfv',
							   frame_or_truss='tesft')
		
		serializer = InputStructureSerializer(struc)
		
		self.assertEqual(serializer.data, {'moment_of_inertia_y': 99.99, \
										   'moment_of_inertia_z': 99.99, \
										   'cross_sectional_area': 99.99, \
										   'y_max': 99.99, \
										   'young_modulus': 99.99, \
										   'shear_modulus': 99.99, \
										   'torsional_constant': 99.99, \
										   'connectivity_table': 'testct', \
										   'nodal_coordinates': 'testnc', \
										   'boundary_conditions': 'testbc', \
										   'force_vector': 'testfv', \
										   'frame_or_truss': 'tesft'})
	
class OutputStructureSerializerTests(TestCase):		
	def test_serializer_with_normal_data(self):
		'''
		Check serializer output with normal data
		'''
		struc = OutputStructure(nodal_coordinates='test123', stress='test123')
		
		serializer = OutputStructureSerializer(struc)
		
		self.assertEqual(serializer.data, {'nodal_coordinates': 'test123', 'stress': 'test123'})
			
# class FeaStructureInputViewTests(TestCase):		
	# def test_Json_input_object(self):
		# '''
		# Check for a valid status given valid data
		# '''
		
		# factory = APIRequestFactory()
		
		# data = {
			# "moment_of_inertia_y":"7363.1078",
			# "moment_of_inertia_z":"7363.1078",
			# "cross_sectional_area":"235.619",
			# "y_max":"10",
			# "young_modulus":"100",
			# "shear_modulus":"100",
			# "torsional_constant":"100",
			# "connectivity_table":"{1 : [1, 2]}",
			# "nodal_coordinates":"{1 : [0,0], 2 : [0,1]}",
			# "boundary_conditions":"[ 0, 1, 2]",
			# "force_vector":"[0, 0, 0, 0, -1, 0]",
			# "frame_or_truss":"frame"
		# }
		# request = factory.post('input/',data, format='json')
		# view = fea_structure_input
		# response = view(request)
		
		# self.assertEqual(response.status_code, 201)
		
class FEA2DOutputViewTests(TestCase):				
	def test_json_output_object(self):
		'''
		Check for a valid status given valid key
		'''
		struc = OutputStructure(nodal_coordinates='test123', stress='test123')
		struc.save()
		id = OutputStructure.objects.all()[0].id
		
		url = 'output/' + str(id)
		
		factory = APIRequestFactory()
		request = factory.get(url)
		view = fea_structure_output
		response = view(request, id)
		
		self.assertEqual(response.status_code, 200)
		
class FeaStructureNodeTests(TestCase):
	def test_fea_node_creation(self):
		'''
		Check for node creation
		'''
		test_node = node(1,2,3,4)
		
		self.assertEqual(test_node.id, 1)
		self.assertEqual(test_node.x, 2)
		self.assertEqual(test_node.y, 3)
		self.assertEqual(test_node.z, 4)
		
class FeaStructureElementTests(TestCase):
	def test_fea_element_creation(self):
		'''
		Check for element creation
		'''
		nodei = node(1,2,3,4)
		nodej = node(2,4,6,7)
		test_element = element(nodei, nodej, 1, 2, 3, 4, 5, 6)
		
		self.assertEqual(test_element.nodei, nodei)
		self.assertEqual(test_element.nodej, nodej)
		self.assertEqual(test_element.E, 1)
		self.assertEqual(test_element.G, 2)
		self.assertEqual(test_element.J, 3)
		self.assertEqual(test_element.Iy, 4)
		self.assertEqual(test_element.Iz, 5)
		self.assertEqual(test_element.A, 6)
		
	def test_fea_element_calc_properties_normal_values(self):
		'''
		Test the calc_properties function with normal values
		'''
		nodei = node(1,0,0,0)
		nodej = node(2,0,1,0)
		test_element = element(nodei, nodej, 1, 2, 3, 4, 5, 6)
		test_element.calc_properties()
		
		self.assertEqual(test_element.L, 1)
		self.assertEqual(test_element.Cxx, 0)
		self.assertEqual(test_element.Cyx, 1)
		self.assertEqual(test_element.Czx, 0)
		
	# def test_fea_element_calc_stiffness_frame_general(self):
		# '''
		# Test the calculation of the stiffness matrix for a frame
		# '''
		# nodei = node(1, 0, 0)
		# nodej = node(2, 0, 10)
		# test_element = element(nodei, nodej, 10, 10, 1)
		# test_element.calc_stiffness_frame()
		
		# equal = (test_element.K == np.matrix([[1.2, 0., 6., -1.2, 0., 6.],
											  # [0., 1., 0., 0., -1., 0.],
											  # [6., 0., 40., -6., 0., 20.],
											  # [-1.2, 0., -6., 1.2, 0., -6.],
											  # [0., -1., 0., 0., 1., 0.],
											  # [6.0, 0., 20., -6., 0., 40.]])).all()

		# self.assertEqual(equal, True)
		
	# def test_fea_element_calc_sitffness_frame_xy_coincide_bigger_jz(self):
	
	# def test_fea_element_calc_sitffness_frame_xy_coincide_smaller_jz(self):
		
	def test_fea_element_calc_stiffness_truss(self):
		'''
		Test the calculation of the stiffness matrix for a frame
		'''
		nodei = node(1, 0, 0, 0)
		nodej = node(2, 4, 3, 0)
		test_element = element(nodei, nodej, 1, 1, 1, 1, 1, 1)
		test_element.E = 10
		test_element.Iy = 10
		test_element.Iz = 10
		test_element.A = 1
		test_element.L = 10
		test_element.Cxx = 1
		test_element.Cyx = 2
		test_element.Czx = 3
		test_element.calc_stiffness_truss()
		
		equal = (test_element.K == np.matrix([[1, 2, 3, -1, -2, -3],
											  [2, 4, 6, -2, -4, -6],
											  [3, 6, 9, -3, -6, -9],
											  [-1, -2, -3, 1, 2, 3],
											  [-2, -4, -6, 2, 4, 6],
											  [-3, -6, -9, 3, 6, 9]])).all()
										  
		self.assertEqual(equal, True)

	
# class FeaStructureFrameTests(TestCase):
	# def test_fea_structure_creation(self):
		# '''
		# Test the creation of the frame object
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max,
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
						   
		# self.assertEqual(test_frame.moment_of_inertia, 10)
		# self.assertEqual(test_frame.cross_sectional_area, 5)
		# self.assertEqual(test_frame.y_max, 10)
		# self.assertEqual(test_frame.modulus_elasticity, 10)
		# self.assertEqual(test_frame.connectivity_table, {1 : [1, 2], 2 : [2, 3]})
		# self.assertEqual(test_frame.nodal_coordinates, {1 : [0,0], 2 : [0,1], 3 : [10,10]})
		# self.assertEqual(test_frame.boundary_conditions, [1,2,3])
		# self.assertEqual(test_frame.force_vector, [0, 0, 0, 0, -1, 0])
		
	# def test_fea_frame_node_creation(self):
		# '''
		# Test the creation of nodes from the nodal_coordinates
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		
		# self.assertEqual([test_frame.nodes[2].id,test_frame.nodes[2].x,test_frame.nodes[2].y], [2,0,1])
		
	# def test_fea_frame_element_creation(self):
		# '''
		# Test the creation of elements from the connectivity_table
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		# test_frame.create_elements()
		
		# self.assertEqual([test_frame.elements[2].nodei.x, test_frame.elements[2].nodei.y], [0, 1])
		
	# def test_fea_frame_element_calc_properties(self):
		# '''
		# Test the calc_properties method of each element
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		
		# self.assertEqual(test_frame.elements[1].L, 1)
		# self.assertEqual(test_frame.elements[1].Cx, 0)
		# self.assertEqual(test_frame.elements[1].Cy, 1)

	# def test_fea_frame_element_calc_stiffness(self):
		# '''
		# Test the calc_stiffness method of each element
		# '''
		# moment_of_inertia = 1
		# cross_sectional_area = 1
		# y_max = 10
		# modulus_elasticity = 1
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		# test_frame.calc_stiffness()
		
		# equal = (test_frame.elements[1].K == np.matrix([[12., 0., 6., -12., 0., 6.],
													    # [0., 1., 0., 0., -1., 0.],
													    # [6., 0., 4., -6., 0., 2.],
													    # [-12., 0., -6., 12., 0., -6.],
													    # [0., -1., 0., 0., 1., 0.],
													    # [6., 0., 2., -6., 0., 4.]])).all()

		# self.assertEqual(equal, True)
		
	# def test_fea_frame_calc_assemblage(self):
		# '''
		# Test the calc_assemblage method for frame
		# '''
		# moment_of_inertia = 1
		# cross_sectional_area = 1
		# y_max = 10
		# modulus_elasticity = 1
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		# test_frame.calc_stiffness()
		# test_frame.elements[2].K = np.matrix([[12., 0., 6., -12., 0., 6.],
											  # [0., 1., 0., 0., -1., 0.],
											  # [6., 0., 4., -6., 0., 2.],
											  # [-12., 0., -6., 12., 0., -6.],
											  # [0., -1., 0., 0., 1., 0.],
											  # [6., 0., 2., -6., 0., 4.]])
		# test_frame.calc_assemblage()
		
		# equal = (test_frame.assemblage == np.matrix([[12., 0., 6., -12., 0., 6., 0., 0., 0.],
													 # [0., 1., 0., 0., -1., 0., 0., 0., 0.],
													 # [6., 0., 4., -6., 0., 2., 0., 0., 0.],
													 # [-12., 0., -6., 24., 0., 0., -12., 0., 6.],
													 # [0., -1., 0., 0., 2., 0., 0., -1., 0.],
													 # [6., 0., 2., 0., 0., 8., -6., 0., 2.],
													 # [0., 0., 0., -12., 0., -6., 12., 0., -6.],
													 # [0., 0., 0., 0., -1., 0., 0., 1., 0.],
													 # [0., 0., 0., 6., 0., 2., -6., 0., 4.]])).all()

		# self.assertEqual(equal, True)
		
	# def test_fea_frame_calc_displacement(self):
		# '''
		# Test the calc_displacement method for frame
		# '''
		# moment_of_inertia = 1000
		# cross_sectional_area = 100
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1,2]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		# test_frame.calc_stiffness()
		# test_frame.calc_assemblage()
		# test_frame.calc_displacement()
		
		# equal = (test_frame.Q.round(6) == np.matrix([[0,0,0,0,-0.001,0]]).transpose()).all()

		# self.assertEqual(equal, True)
		# # self.assertIs(test_frame.Q,1)
		# self.assertEqual(len(test_frame.Q), 6)
		
	# def test_fea_frame_calc_stress(self):
		# '''
		# Test the calc_stress method for frame
		# '''
		# moment_of_inertia = 490.87385
		# cross_sectional_area = 78.53982
		# y_max = 5
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1,2]
		# force_vector = [ 0, 0, 0, 0, -1, 0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
						   
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		# test_frame.calc_stiffness()
		# test_frame.calc_assemblage()
		# test_frame.calc_displacement()
		# test_frame.calc_stress()
		
		# self.assertEqual(round(test_frame.stress[1][0],4), 0.0127)
		
	# def test_fea_frame_test_calc_new_nodal_coordinates_real_data(self):
		# '''
		# Test the calc_stress method for frame
		# '''
		# moment_of_inertia = 30.7
		# cross_sectional_area = 20
		# y_max = 2.5
		# modulus_elasticity = 10000
		# connectivity_table = {1:[1,2],2:[2,3],3:[3,4],4:[4,5],5:[5,6],6:[6,7],7:[7,8],8:[8,1],9:[8,3],10:[2,7],11:[3,6],12:[7,4]}
		# nodal_coordinates = {1:[-200,0],2:[-100,100],3:[0,100],4:[100,100],5:[200,0],6:[100,0],7:[0,0],8:[-100,0]}
		# boundary_conditions = [0,1,13]
		# force_vector = [0,0,0,0,-50000,0,0,0,0,0,-50000,0,0,0,0,0,0,0,0,50000,0,0,0,0]
		
		# test_frame = frame(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
						   
		# test_frame.create_nodes()
		# test_frame.create_elements()
		# test_frame.calc_properties()
		# test_frame.calc_stiffness()
		# test_frame.calc_assemblage()
		# test_frame.calc_displacement()
		# test_frame.calc_new_nodal_coordinates()
		
		# self.assertEqual(test_frame.new_nodal_coordinates[7][1] != 0 , True)

# class FEA2DTrussTests(TestCase):
	# def test_fea_truss_calc_assemblage(self):
		# '''
		# Test the calc_assemblage method for truss
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 1
		# connectivity_table = {1 : [1, 2], 2 : [2, 3]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [10,10]}
		# boundary_conditions = [1,2,3]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_truss = truss(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_truss.create_nodes()
		# test_truss.create_elements()

		# test_truss.elements[1].K = np.matrix([[1., 1., 1., 1.],
											  # [1., 1., 1., 1.],
											  # [1., 1., 1., 1.],
											  # [1., 1., 1., 1.]])

		# test_truss.elements[2].K = np.matrix([[1., 1., 1., 1.],
											  # [1., 1., 1., 1.],
											  # [1., 1., 1., 1.],
											  # [1., 1., 1., 1.]])
		# test_truss.calc_assemblage()
		
		# equal = (test_truss.assemblage == np.matrix([[1., 1., 1., 1., 0., 0.],
													 # [1., 1., 1., 1., 0., 0.],
													 # [1., 1., 2., 2., 1., 1.],
													 # [1., 1., 2., 2., 1., 1.],
													 # [0., 0., 1., 1., 1., 1.],
													 # [0., 0., 1., 1., 1., 1.]])).all()

		# self.assertEqual(equal, True)
		
	# def test_fea_truss_calc_stress(self):
		# '''
		# Test the calc_stress method for truss
		# '''
		# moment_of_inertia = 490.87385
		# cross_sectional_area = 78.53982
		# y_max = 5
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1]
		# force_vector = [ 0, 0, 0, -1]
		
		# test_truss = truss(moment_of_inertia, cross_sectional_area, y_max, 
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
						   
		# test_truss.create_nodes()
		# test_truss.create_elements()
		# test_truss.calc_properties()
		# test_truss.calc_stiffness()
		# test_truss.calc_assemblage()
		# test_truss.calc_displacement()
		# test_truss.calc_stress()
		
		# self.assertEqual(round(test_truss.stress[1][0],4), -0.0127)
		
	# def test_fea_truss_calc_new_nodal_coordinates(self):
		# '''
		# Test the calc_new_nodal_coordinates method
		# '''
		# moment_of_inertia = 10
		# cross_sectional_area = 5
		# y_max = 10
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2], 2 : [2, 3], 3 : [3, 4], 4 : [4, 5]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1], 3 : [1,2], 4 : [4,5], 5 : [10, 10]}
		# boundary_conditions = [0,1,2]
		# force_vector = [0, 0, 0, 0, -1, 0]
		
		# test_truss = truss(moment_of_inertia, cross_sectional_area, y_max,
						   # modulus_elasticity, connectivity_table, nodal_coordinates,
						   # boundary_conditions, force_vector)
		
		# test_truss.Q = np.matrix([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]).transpose()
		# test_truss.calc_new_nodal_coordinates()
		
		# self.assertEqual(test_truss.new_nodal_coordinates, {1 : [1,1], 2 : [1,2], 3 : [2,3], 4 : [5,6], 5 : [11, 11]})
		# # self.assertIs(test_truss.Q, 1)

# class FEA2DFeaTests(TestCase):		
	# def test_fea_fea_data_validate_force_error(self):
		# '''
		# Test the data_validate method; force vector error
		# '''
		
		# moment_of_inertia = 30
		# cross_sectional_area = 20
		# y_max = 15
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1]
		# force_vector = [0, 0, 0, -1, 0]
		# frame_or_truss = 'frame'
		
		# test_fea = fea(moment_of_inertia, cross_sectional_area, y_max, 
					   # modulus_elasticity, connectivity_table, nodal_coordinates,
					   # boundary_conditions, force_vector, frame_or_truss)
					   
		

		# self.assertEqual(test_fea.analyze(), "ERROR: size of force vector too small, require 3*(# of nodes)")
	
	# def test_fea_fea_analyze_frame(self):
		# '''
		# Test the analyze method for the fea class
		# '''
		
		# moment_of_inertia = 490.87385
		# cross_sectional_area = 78.53982
		# y_max = 5
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1]
		# force_vector = [ 0, 0, 0, 0, -1, 0]
		# frame_or_truss = 'frame'
		
		# test_fea = fea(moment_of_inertia, cross_sectional_area, y_max, 
					   # modulus_elasticity, connectivity_table, nodal_coordinates,
					   # boundary_conditions, force_vector, frame_or_truss)
					   
		# test_fea.analyze()

		# self.assertEqual(round(test_fea.struc.stress[1][0],4), 0.0127)
		
	# def test_fea_fea_analyze_truss(self):
		# '''
		# Test the analyze method for the fea class
		# '''
		
		# moment_of_inertia = 490.87385
		# cross_sectional_area = 78.53982
		# y_max = 5
		# modulus_elasticity = 10
		# connectivity_table = {1 : [1, 2]}
		# nodal_coordinates = {1 : [0,0], 2 : [0,1]}
		# boundary_conditions = [0,1]
		# force_vector = [ 0, 0, 0, -1]
		# frame_or_truss = 'truss'
		
		# test_fea = fea(moment_of_inertia, cross_sectional_area, y_max,
					   # modulus_elasticity, connectivity_table, nodal_coordinates,
					   # boundary_conditions, force_vector, frame_or_truss)
					   
		# test_fea.analyze()
		
		# self.assertEqual(round(test_fea.struc.stress[1],4), -0.0127)
		# # self.assertIs(test_fea.struc.new_nodal_coordinates, 1)