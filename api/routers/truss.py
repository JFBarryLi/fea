from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Optional

from fea.truss.truss import Truss
from .truss_example import TrussExampleInput

router = APIRouter()


class EleProp(BaseModel):
    index: int
    E: float
    A: float


class Node(BaseModel):
    index: int
    x: float
    y: float
    z: float


class Connect(BaseModel):
    index: int
    i: str
    j: str


class Vector(BaseModel):
    index: int
    value: float


class NodeForces(BaseModel):
    index: int
    forces: Dict[str, Vector]


class NodeBc(BaseModel):
    index: int
    bc: Dict[str, Vector]


class TrussData(BaseModel):
    matProp: Dict[str, EleProp]
    nodalCoords: Dict[str, Node]
    connectivity: Dict[str, Connect]
    forceVector: Dict[str, NodeForces]
    boundaryConditions: Dict[str, NodeBc]
    stresses: Optional[Dict[str, float]] = None

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
    t = Truss(
        truss_dict['matProp'],
        truss_dict['nodalCoords'],
        truss_dict['connectivity'],
        truss_dict['forceVector'],
        truss_dict['boundaryConditions']
    )

    t.solve_truss()

    truss.nodalCoords = t.deformed_nodal_coords
    truss.stresses = t.stresses
    return truss
