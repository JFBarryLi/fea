from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from fea.truss.truss import Truss
from .truss_example import TrussExampleInput

router = APIRouter()


class MatProp(BaseModel):
    ele: str
    E: float
    A: float


class Node(BaseModel):
    id: str
    x: float
    y: float
    z: float


class Connect(BaseModel):
    id: str
    i: str
    j: str


class ForceVector(BaseModel):
    node: str
    u1: float
    u2: float
    u3: float


class BoundaryCondition(BaseModel):
    node: str
    u1: bool
    u2: bool
    u3: bool


class Stress(BaseModel):
    ele: str
    vm: float


class TrussData(BaseModel):
    matProp: List[MatProp]
    nodalCoords: List[Node]
    connectivity: List[Connect]
    forceVector: List[ForceVector]
    boundaryConditions: List[BoundaryCondition]
    stresses: Optional[List[Stress]] = None

    class Config:
        schema_extra = {
            "example": TrussExampleInput
        }


@router.get('/')
def truss_root():
    return 'Truss Solver'


@router.post('/', response_model=TrussData)
def truss_solve(truss: TrussData):
    truss_dict = truss.dict()

    mat_prop = convert_to_dict(truss_dict['matProp'], 'ele')
    nodal_coords = convert_to_dict(truss_dict['nodalCoords'], 'id')
    connectivity = convert_to_dict(truss_dict['connectivity'], 'id')
    force_vector = convert_to_dict(truss_dict['forceVector'], 'node')
    boundary_conditions = convert_to_dict(
        truss_dict['boundaryConditions'],
        'node'
    )

    t = Truss(
        mat_prop,
        nodal_coords,
        connectivity,
        force_vector,
        boundary_conditions
    )

    t.solve_truss()

    truss.matProp = convert_to_list(t.mat_prop, 'ele')
    truss.nodalCoords = convert_to_list(t.deformed_nodal_coords, 'id')
    truss.connectivity = convert_to_list(t.connectivity, 'id')
    truss.forceVector = convert_to_list(t.force_vector, 'node')
    truss.boundaryConditions = convert_to_list(t.boundary_conditions, 'node')
    truss.stresses = [{'ele': s, 'vm': t.stresses[s]} for s in t.stresses]
    return truss


def convert_to_dict(list, key):
    dict = {}
    for item in list:
        dict[item[key]] = {i: item[i] for i in item if i != key}

    return dict


def convert_to_list(dict, key):
    list = []
    for k in dict:
        new_dict = {i: dict[k][i] for i in dict[k]}
        new_dict[key] = k
        list.append(new_dict)
