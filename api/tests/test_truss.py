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
