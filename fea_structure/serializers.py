'''
Serializer
'''

from rest_framework import serializers
from fea_structure.models import InputStructure, OutputStructure

class InputStructureSerializer(serializers.ModelSerializer):
	class Meta:
		model = InputStructure
		fields = ('outer_diameter', 'inner_diameter', 'modulus_elasticity',
				  'connectivity_table', 'nodal_coordinates', 'boundary_conditions',
				  'force_vector', 'frame_or_truss')
		
class OutputStructureSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutputStructure
		fields = ('nodal_coordinates', 'stress')