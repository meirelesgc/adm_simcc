from tests.factories.institution_factory import InstitutionFactory
from http import HTTPStatus


def test_insert_single_institution(client):
    institution = InstitutionFactory.create_batch(1)
    response = client.post("/InstitutionRest/Insert", json=institution)

    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_constrain_institution(client):
    institution = InstitutionFactory.create_batch(1)
    response = client.post("/InstitutionRest/Insert", json=institution)
    response = client.post("/InstitutionRest/Insert", json=institution)

    assert response.status_code == HTTPStatus.CONFLICT


def test_insert_some_institutions(client):
    institution = InstitutionFactory.create_batch(3)
    response = client.post("/InstitutionRest/Insert", json=institution)
    assert response.status_code == HTTPStatus.CREATED


def test_query_institutions(client):
    institution = InstitutionFactory.create_batch(1)
    response = client.post("/InstitutionRest/Insert", json=institution)

    institution_id = institution[0]["institution_id"]
    endpoint = f"/InstitutionRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json == institution[0]


def test_query_institutions_full_data(client):
    institution = InstitutionFactory.create_batch(1)
    response = client.post("/InstitutionRest/Insert", json=institution)

    institution_id = institution[0]["institution_id"]
    endpoint = f"/InstitutionRest/Query/Count?institution_id={institution_id}"
    response = client.get(endpoint)

    data = [
        {
            "name": institution[0]["name"],
            "institution_id": institution[0]["institution_id"],
            "count_gp": 0,
            "count_gpr": 0,
            "count_r": 0,
        }
    ]
    assert response.status_code == HTTPStatus.OK
    assert (response.json) == data
