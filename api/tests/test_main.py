from fastapi.testclient import TestClient

from api.main import fea_app

client = TestClient(fea_app)


def test_app_root():
    response = client.get('/')
    assert response.status_code == 200
