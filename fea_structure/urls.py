from django.urls import path
from fea_structure import views

urlpatterns = [
    path('fea/structure/input/', views.fea_structure_input),
	path('fea/structure/output/<int:output_structure_id>', views.fea_structure_output),
]
