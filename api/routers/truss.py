import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator, Field
from typing import List, Optional

from fea.truss.truss import Truss
from .truss_example import TrussExampleInput

log = logging.getLogger(__name__)

router = APIRouter()


class MatProp(BaseModel):
    ele: str = Field(title='Element')
    E: float = Field(title="Young's Modulus")
    A: float = Field(title='Cross Sectional Area')


class Node(BaseModel):
    id: str = Field(title='Node Id')
    x: float = Field(title='x coord')
    y: float = Field(title='y coord')
    z: float = Field(title='z coord')


class Connect(BaseModel):
    id: str = Field(title='Element Id')
    i: str = Field(title='Node i')
    j: str = Field(title='Node j')


class ForceVector(BaseModel):
    node: str = Field(title='Node')
    u1: float = Field(title='Fx')
    u2: float = Field(title='Fy')
    u3: float = Field(title='Fz')


class BoundaryCondition(BaseModel):
    node: str = Field(title='Node')
    u1: bool = Field(title='x constraint')
    u2: bool = Field(title='y constraint')
    u3: bool = Field(title='z constraint')


class Stress(BaseModel):
    ele: str = Field(title='Element')
    vm: float = Field(title='Von Mises Stress')


class TrussData(BaseModel):
    matProp: List[MatProp] = Field(title='Material Property')
    nodalCoords: List[Node] = Field(title='Nodal Coordinates')
    connectivity: List[Connect] = Field(title='Element Connectivity')
    forceVector: List[ForceVector] = Field(title='Force Vector')
    boundaryConditions: List[BoundaryCondition] = Field(
        title='Boundary Conditions'
    )
    stresses: Optional[List[Stress]] = Field(None, title='Stresses')

    class Config:
        schema_extra = {
            "example": TrussExampleInput
        }

    @validator('matProp')
    def validate_unique_mat_prop_id(cls, v):
        if check_for_unique_key(v, 'ele'):
            return v
        else:
            raise ValueError('Key must be unique.')

    @validator('nodalCoords')
    def validate_unique_nodal_coords_id(cls, v):
        if check_for_unique_key(v, 'id'):
            return v
        else:
            raise ValueError('Key must be unique.')

    @validator('connectivity')
    def validate_unique_connectivity_id(cls, v):
        if check_for_unique_key(v, 'id'):
            return v
        else:
            raise ValueError('Key must be unique.')

    @validator('boundaryConditions')
    def validate_unique_boundary_conditions_id(cls, v):
        if check_for_unique_key(v, 'node'):
            return v
        else:
            raise ValueError('Key must be unique.')

    @validator('stresses')
    def validate_unique_stresses_id(cls, v):
        if check_for_unique_key(v, 'ele'):
            return v
        else:
            raise ValueError('Key must be unique.')


def check_for_unique_key(list, key):
    key_list = [dict(item)[key] for item in list]
    return len(set(key_list)) == len(key_list)


@router.get('/')
def truss_root():
    return 'Truss Solver'


@router.post('/', response_model=TrussData)
def truss_solve(truss: TrussData):
    truss_dict = truss.dict()

    mat_prop = convert_to_dict(truss_dict['matProp'], 'ele')
    nodal_coords = convert_to_dict(truss_dict['nodalCoords'], 'id')
    connectivity = convert_to_dict(truss_dict['connectivity'], 'id')
    force_vector = truss_dict['forceVector']
    boundary_conditions = truss_dict['boundaryConditions']

    try:
        t = Truss(
            mat_prop,
            nodal_coords,
            connectivity,
            force_vector,
            boundary_conditions
        )

        t.solve_truss()
    except Exception as e:
        log.error({e})
        raise HTTPException(
            status_code=500,
            detail=f'Error: {e}',
        )

    truss.matProp = convert_to_list(t.mat_prop, 'ele')
    truss.nodalCoords = convert_to_list(t.deformed_nodal_coords, 'id')
    truss.connectivity = convert_to_list(t.connectivity, 'id')
    truss.forceVector = t.force_vector
    truss.boundaryConditions = t.boundary_conditions
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

    return list
