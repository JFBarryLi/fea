from django.test import TestCase

from .models import InputStructure, OutputStructure
from .serializers import InputStructureSerializer, OutputStructureSerializer
from .views import FEA2D_input, FEA2D_output

from rest_framework.test import APIRequestFactory
	
class InputStructureModelTests(TestCase):

	def test_object_creation_with_normal_values(self):
		'''
		Check that InputStructure objects are created and saved properly
		'''
		struc = InputStructure(ip_address='999.999.999.999', 
								outer_diameter=99.99,
								inner_diameter=99.99,
								modulus_elasticity=99.99,
								yield_strength=99.99,
								connectivity_table='testct',
								nodal_coordinates='testnc',
								boundary_conditions='testbc',
								frame_or_truss='tesft')
		
		self.assertEqual(struc.ip_address, '999.999.999.999')
		self.assertEqual(struc.outer_diameter, 99.99)
		self.assertEqual(struc.inner_diameter, 99.99)
		self.assertEqual(struc.modulus_elasticity, 99.99)
		self.assertEqual(struc.yield_strength, 99.99)
		self.assertEqual(struc.connectivity_table, 'testct')
		self.assertEqual(struc.nodal_coordinates, 'testnc')
		self.assertEqual(struc.boundary_conditions, 'testbc')
		self.assertEqual(struc.frame_or_truss, 'tesft')
	
	def test_object_save(self):
		'''
		Check InputStructure are saved properly
		'''
		struc = InputStructure(ip_address='999.999.999.999', 
								outer_diameter=99.99,
								inner_diameter=99.99,
								modulus_elasticity=99.99,
								yield_strength=99.99,
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
		struc = OutputStructure(nodal_coordinates='test123', factor_of_safety=99.99)
		
		self.assertEqual(struc.nodal_coordinates, 'test123')
		self.assertEqual(struc.factor_of_safety, 99.99)
	
	def test_object_save(self):
		'''
		Check OutputStructure are saved properly
		'''
		struc = OutputStructure(nodal_coordinates='test123', factor_of_safety=99.99)
		struc.save()
		
		self.assertEqual(OutputStructure.objects.order_by('created')[0].nodal_coordinates, 'test123')
		
class InputStructureSerializerTests(TestCase):
	def test_serializer_with_normal_data(self):
		'''
		Check serializer output with normal data
		'''
		struc = InputStructure(ip_address='999.999.999.999', 
								outer_diameter=99.99,
								inner_diameter=99.99,
								modulus_elasticity=99.99,
								yield_strength=99.99,
								connectivity_table='testct',
								nodal_coordinates='testnc',
								boundary_conditions='testbc',
								frame_or_truss='tesft')
		
		serializer = InputStructureSerializer(struc)
		
		self.assertEqual(serializer.data, {'ip_address': '999.999.999.999', 'outer_diameter': '99.99', 'inner_diameter': '99.99', 'modulus_elasticity': '99.99', 'yield_strength': '99.99', 'connectivity_table': 'testct', 'nodal_coordinates': 'testnc', 'boundary_conditions': 'testbc', 'frame_or_truss': 'tesft'})
	
class OutputStructureSerializerTests(TestCase):		
	def test_serializer_with_normal_data(self):
		'''
		Check serializer output with normal data
		'''
		struc = OutputStructure(nodal_coordinates='test123', factor_of_safety=99.99)
		
		serializer = OutputStructureSerializer(struc)
		
		self.assertEqual(serializer.data, {'nodal_coordinates': 'test123', 'factor_of_safety': '99.99'})
			
class FEA2DInputViewTests(TestCase):		
	def test_Json_input_object(self):
		'''
		Check for a valid status given valid data
		'''
		
		factory = APIRequestFactory()
		
		data = {
			"ip_address":"999.999.999.999", 
			"outer_diameter":"99.99",
			"inner_diameter":"99.99",
			"modulus_elasticity":"99.99",
			"yield_strength":"99.99",
			"connectivity_table":"testct",
			"nodal_coordinates":"testnc",
			"boundary_conditions":"testbc",
			"frame_or_truss":"tesft"
		}
		request = factory.post('input/',data, format='json')
		view = FEA2D_input
		response = view(request)
		
		self.assertEqual(response.status_code, 201)
		
class FEA2DOutputViewTests(TestCase):				
	def test_json_output_object(self):
		'''
		Check for a valid status given valid key
		'''
		struc = OutputStructure(nodal_coordinates='test123', factor_of_safety=99.99)
		struc.save()
		id = OutputStructure.objects.all()[0].id
		
		url = 'output/' + str(id)
		
		factory = APIRequestFactory()
		request = factory.get(url)
		view = FEA2D_output
		response = view(request, id)
		
		self.assertEqual(response.status_code, 200)