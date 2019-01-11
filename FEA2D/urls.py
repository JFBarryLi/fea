from django.urls import path
from FEA2D import views

urlpatterns = [
    path('input/', views.fea2d_input),
	path('output/<int:output_structure_id>', views.fea2d_output),
]
