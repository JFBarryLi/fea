from FEA2D.models import InputStructure, OutputStructure, InputOutputLink
from FEA2D.serializers import InputStructureSerializer, OutputStructureSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .fea import node, element, structure, frame, truss, fea

@api_view(['POST'])
def FEA2D_input(request):
	'''
	Create a InputStructure, perform FEA2D and return an OutputStructure
	'''
	
	if request.method == 'POST':
		serializer = InputStructureSerializer(data=request.data)
		if serializer.is_valid():
			instance = serializer.save()
			
			# Finite element analysis 2D
			outer_diameter = instance.outer_diameter
			inner_diameter = instance.inner_diameter
			modulus_elasticity = instance.modulus_elasticity
			yield_strength = instance.yield_strength
			connectivity_table = eval(instance.connectivity_table)
			nodal_coordinates = eval(instance.nodal_coordinates)
			boundary_conditions = eval(instance.boundary_conditions)
			force_vector = eval(instance.force_vector)
			frame_or_truss = instance.frame_or_truss
			
			struc = fea(outer_diameter, inner_diameter, modulus_elasticity,
						yield_strength, connectivity_table, nodal_coordinates,
						boundary_conditions, force_vector, frame_or_truss)
			struc.analyze()
			
			output_struc = OutputStructure(nodal_coordinates=struc.new_nodal_coordinates, stress=struc.stress)
			output_struc.save()
			
			# Save InputStructure.id and OutputStructure.id
			io_link = InputOutputLink(input_id=instance.id, output_id=output_struc.id)
			
			return Response(output_struc.id, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def FEA2D_output(request, output_structure_id):
	'''
	Retrieve OutputStructure corresponding to the InputStructure
	'''
	try:
		output_structure = OutputStructure.objects.get(pk=output_structure_id)
	except OutputStructure.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	
	if request.method == 'GET':
		serializer = OutputStructureSerializer(output_structure)
		return Response(serializer.data)
		
