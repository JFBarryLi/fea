'''
Serializer
'''

from rest_framework import serializers
from FEA2D.models import InputStructure, OutputStructure

class InputStructureSerializer(serializers.ModelSerializer):
	class Meta:
		model = InputStructure
		fields = ('ip_address', 'outer_diameter', 'inner_diameter', 'modulus_elasticity', 'yield_strength', 'connectivity_table', 'nodal_coordinates', 'boundary_conditions', 'force_vector', 'frame_or_truss')
		
class OutputStructureSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutputStructure
		fields = ('nodal_coordinates', 'stress')