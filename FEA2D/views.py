from FEA2D.models import InputStructure, OutputStructure
from FEA2D.serializers import InputStructureSerializer, OutputStructureSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

@api_view(['POST'])
def FEA2D_input(request):
	'''
	Create a InputStructure, perform FEA2D and return an OutputStructure
	'''
	
	if request.method == 'POST':
		serializer = InputStructureSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			
			# PERFORM FEA HERE
			# GRAB OUTPUTSTRUCTURE PK AND RETURN IT
			
			return Response(serializer.data, status=status.HTTP_201_CREATED)
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
		
