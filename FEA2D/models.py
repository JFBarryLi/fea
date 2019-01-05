from django.db import models

class InputStructure(models.Model):
	'''
	Input structure
	'''

	created = models.DateTimeField(auto_now_add=True)
	ip_address = models.CharField(max_length=50)
	outer_diameter = models.DecimalField(max_digits=10, decimal_places=2)
	inner_diameter = models.DecimalField(max_digits=10, decimal_places=2)
	modulus_elasticity = models.DecimalField(max_digits=10, decimal_places=2)
	yield_strength = models.DecimalField(max_digits=10, decimal_places=2)
	connectivity_table = models.TextField()
	nodal_coordinates = models.TextField()
	boundary_conditions = models.TextField()
	frame_or_truss = models.CharField(max_length=5)
	
	class Meta:
		ordering = ('created',)
		
class OutputStructure(models.Model):
	'''
	Output structure
	'''

	created = models.DateTimeField(auto_now_add=True)
	nodal_coordinates = models.TextField()
	factor_of_safety = models.DecimalField(max_digits=10, decimal_places=2)
	
	class Meta:
		ordering = ('created',)
		
