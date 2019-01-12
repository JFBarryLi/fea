from django.db import models
import time, random

START_TIME = int(time.time()*1000)

def gen_id():
	'''
	Generate unique primary key
	'''

	t = int(time.time()*1000) - START_TIME
	u = random.SystemRandom().getrandbits(23)
	id = (t << 23 ) | u

	return id

class InputStructure(models.Model):
	'''
	Input structure
	'''
	
	id = models.BigIntegerField(default = gen_id, primary_key=True)  
	created = models.DateTimeField(auto_now_add=True)
	outer_diameter = models.FloatField()
	inner_diameter = models.FloatField()
	modulus_elasticity = models.FloatField()
	connectivity_table = models.TextField()
	nodal_coordinates = models.TextField()
	boundary_conditions = models.TextField()
	force_vector = models.TextField()
	frame_or_truss = models.CharField(max_length=5)
	
	class Meta:
		ordering = ('created',)
		
class OutputStructure(models.Model):
	'''
	Output structure
	'''
	
	id = models.BigIntegerField(default = gen_id, primary_key=True)  
	created = models.DateTimeField(auto_now_add=True)
	nodal_coordinates = models.TextField()
	stress = models.TextField()

	class Meta:
		ordering = ('created',)
		
class InputOutputLink(models.Model):
	'''
	Link between InputStructure and OutputStructure
	'''
	
	id = models.BigIntegerField(default = gen_id, primary_key=True)  
	created = models.DateTimeField(auto_now_add=True)
	input_id = models.BigIntegerField()
	output_id = models.BigIntegerField()

	class Meta:
		ordering = ('created',)
		