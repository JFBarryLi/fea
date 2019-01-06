from django.urls import path
from FEA2D import views

urlpatterns = [
    path('input/', views.FEA2D_input),
	path('output/<int:output_structure_id>', views.FEA2D_output),
]
