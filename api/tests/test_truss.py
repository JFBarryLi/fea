from copy import deepcopy

from fastapi.testclient import TestClient

from api.main import fea_app
from api.routers.truss_example import TrussExampleInput
from api.routers.truss_example import TrussExampleOutput

client = TestClient(fea_app)


def test_truss_root():
    response = client.get('/truss')
    assert response.status_code == 200


def test_truss_solve():
    response = client.post(
        '/truss/',
        json=TrussExampleInput
    )
    assert response.status_code == 200
    assert response.json() == TrussExampleOutput


def test_validate_unique_mat_prop_id():
    unique_violation_truss = deepcopy(TrussExampleInput)
    unique_violation_truss['matProp'][1]['ele'] = 'ele1'

    response = client.post(
        '/truss/',
        json=unique_violation_truss
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'


def test_validate_unique_nodal_coords_id():
    unique_violation_truss = deepcopy(TrussExampleInput)
    unique_violation_truss['nodalCoords'][1]['id'] = 'node1'

    response = client.post(
        '/truss/',
        json=unique_violation_truss
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'


def test_validate_unique_connectivity_id():
    unique_violation_truss = deepcopy(TrussExampleInput)
    unique_violation_truss['connectivity'][1]['id'] = 'ele1'

    response = client.post(
        '/truss/',
        json=unique_violation_truss
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'


def test_validate_unique_boundary_conditions_id():
    unique_violation_truss = deepcopy(TrussExampleInput)
    unique_violation_truss['boundaryConditions'][1]['node'] = 'node1'

    response = client.post(
        '/truss/',
        json=unique_violation_truss
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'


def test_validate_unique_stresses_id():
    unique_violation_truss = deepcopy(TrussExampleInput)
    unique_violation_truss['stresses'] = [{
            "ele": "ele1",
            "vm": 1
        }, {
            "ele": "ele1",
            "vm": 1
        }
    ]

    response = client.post(
        '/truss/',
        json=unique_violation_truss
    )

    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'
