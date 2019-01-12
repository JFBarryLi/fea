from django.urls import path
from fea_structure import views

urlpatterns = [
    path('input/', views.fea_structure_input),
	path('output/<int:output_structure_id>', views.fea_structure_output),
]
