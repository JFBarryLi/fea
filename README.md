# FEA_WebApp

REST API written with django REST framework

Calculates stress and nodal displacements for a frame or truss structure using finite element analysis


### API Endpoints

#### /input/

Create an InputStructure, perform finite element analysis and return an OutputStructure

Allow: OPTIONS, POST  
Content-Type: application/json  

Content payload example:
```bash
{
	"outer_diameter":"20",
	"inner_diameter":"10",
	"modulus_elasticity":"100",
	"connectivity_table":"{1 : [1, 2]}",
	"nodal_coordinates":"{1 : [0,0], 2 : [0,1]}",
	"boundary_conditions":"[ 0, 1, 2]",
	"force_vector":"[0, 0, 0, 0, -1, 0]",
	"frame_or_truss":"frame"
}
```

Parameters:
  * outer_diameter : float [mm]  
  * inner_diameter : float [mm]  
  * modulus_elasticity : float [MPa]  
  * connectivity_table : dict  
	+ Dictionary representing the 2 nodes associated with each element  
	{element_id : [nodei_id, nodej_id],...}  
  * nodal_coordinates : dict  
	+ Dictionary representing the coordinates of each node  
	{node_id1 : [x1, y1],...}  
  * boundary_conditions : list  
	+ List representing the boundary conditions  
	[0,15,22,...]  
	+ The array determines which DOF are fixed  
	+ For frame each node has 3 degree of freedom:  
		+ index 0 correspond to node_1 x-direction  
		+ index 1 correspond to node_1 y-direction  
		+ index 2 correspond to node_1 theta  
		+ index 3 correspond to node_2 x-direction ...  
	+ For truss each node has 2 degree of freedom:  
		+ index 0 correspond to node_1 x-direction  
		+ index 1 correspond to node_1 y-direction  
		+ index 2 correspond to node_2 x-direction ...  
  * force_vector : list  
	+ List representing the input force into the structure  
	[fx1, fy1, M1, ...]  
  * frame_or_truss : char  
	+ Specifies which type of structure to create  
  
POST request to /input/ returns output_id that identifies the output structure

#### /outout/output_id

Retrieve OutputStructure corresponding to the InputStructure

Allow: GET, OPTIONS  
Content-Type: application/json

Content example:
```bash
{
    "nodal_coordinates": "{1: [0.0, 0.0], 2: [0.0, -3.2441318157838754]}",
    "stress": "{1: [424.41318157838754]}"
}
```
Output:
  * nodal_coordinates : dict  
	+ Dictionary representing the coordinates of each node  
	{node_id1 : [x1, y1],...}
  * stress : dict  
	+ Dictionary representing the stress at each element  
	{ele1 : [stress1],...}

### Installation

```bash
git clone https://github.com/JFBarryLi/FEA2D_WebApp.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:
```bash
python manage.py migrate
```