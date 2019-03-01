from fea_structure.models import InputStructure, OutputStructure, InputOutputLink
from fea_structure.serializers import InputStructureSerializer, OutputStructureSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .fea import node, element, structure, frame, truss, fea

@api_view(['POST'])
def fea_structure_input(request):
	'''
	Create an InputStructure, perform finite element analysis and return an OutputStructure
	'''
	
	if request.method == 'POST':
		serializer = InputStructureSerializer(data=request.data)
		if serializer.is_valid():
			instance = serializer.save()
			
			# Structural finite element analysis
			moment_of_inertia_y = instance.moment_of_inertia_y
			moment_of_inertia_z = instance.moment_of_inertia_z
			cross_sectional_area = instance.cross_sectional_area
			y_max = instance.y_max
			young_modulus = instance.young_modulus
			shear_modulus = instance.shear_modulus
			torsional_constant = instance.torsional_constant
			connectivity_table = eval(instance.connectivity_table)
			nodal_coordinates = eval(instance.nodal_coordinates)
			boundary_conditions = eval(instance.boundary_conditions)
			force_vector = eval(instance.force_vector)
			frame_or_truss = instance.frame_or_truss
			
			struc = fea(moment_of_inertia_y, moment_of_inertia_z, cross_sectional_area, y_max,
						young_modulus, shear_modulus, torsional_constant, connectivity_table, nodal_coordinates,
						boundary_conditions, force_vector, frame_or_truss)
			struc.analyze()
			
			output_struc = OutputStructure(nodal_coordinates=struc.new_nodal_coordinates, stress=struc.stress)
			output_struc.save()
			
			# Save InputStructure.id and OutputStructure.id
			io_link = InputOutputLink(input_id=instance.id, output_id=output_struc.id)
			io_link.save()
			
			return Response(output_struc.id, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fea_structure_output(request, output_structure_id):
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
		
