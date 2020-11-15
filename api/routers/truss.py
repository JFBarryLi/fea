from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from fea.truss.truss import Truss

router = APIRouter()


class EleProp(BaseModel):
    index: int
    E: float
    A: float


class MatProps(BaseModel):
    __root__: Dict[int, EleProp]


class Node(BaseModel):
    index: int
    x: float
    y: float
    z: float


class NodalCoords(BaseModel):
    __root__: Dict[str, Node]


class Connect(BaseModel):
    index: int
    i: int
    j: int


class Connectivity(BaseModel):
    __root__: Dict[str, Connect]


class Vector(BaseModel):
    index: int
    value: float


class Vectors(BaseModel):
    __root__: Dict[str, Vector]


class NodeForces(BaseModel):
    index: int
    forces: Vectors


class NodeBc(BaseModel):
    index: int
    bc: Vectors


class ForceVector(BaseModel):
    __root__: Dict[str, NodeForces]


class BoundaryConditions(BaseModel):
    __root__: Dict[str, NodeBc]


class TrussData(BaseModel):
    matProp: MatProps
    nodalCoords: NodalCoords
    connectivity: Connectivity
    forceVector: ForceVector
    boundaryConditions: BoundaryConditions


@router.get('/')
def truss_root():
    return 'Truss Solver'


@router.post('/')
def truss_solve(truss: TrussData):
    return TrussData
