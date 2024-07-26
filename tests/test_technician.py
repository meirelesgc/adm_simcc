from tests.factories.technician_factory import TechnicianFactory
from http import HTTPStatus


def test_insert_single_technician(client):
    technician = TechnicianFactory.create_batch(1)
    response = client.post("/tecnicos", json=technician)

    assert response.status_code == HTTPStatus.CREATED


def test_insert_single_technician(client):
    technician = TechnicianFactory.create_batch(2)
    response = client.post("/tecnicos", json=technician)
    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_technician(client):
    technician = TechnicianFactory.create_batch(2, matric=123456)
    response = client.post("/tecnicos", json=technician)
    assert response.status_code == HTTPStatus.CONFLICT
