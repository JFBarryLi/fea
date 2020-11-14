from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from fea.truss.truss import Truss

router = APIRouter()


class EleProp(BaseModel):
    E: float
    A: float


class MatProps(BaseModel):
    __root__: Dict[int, EleProp]


class Node(BaseModel):
    x: float
    y: float
    z: float


class NodalCoords(BaseModel):
    __root__: Dict[int, Node]


class Connect(BaseModel):
    i: int
    j: int


class Connectivity(BaseModel):
    __root__: Dict[int, Connect]


class Vector(BaseModel):
    __root__: Dict[int, float]


class ForceVector(BaseModel):
    __root__: Dict[int, Vector]


class BoundaryConditions(BaseModel):
    __root__: Dict[int, Vector]


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
