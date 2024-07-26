from tests.factories.teacher_factory import TeacherFactory
from http import HTTPStatus


def test_insert_single_teacher(client):
    teacher = TeacherFactory.create_batch(1)
    response = client.post("/docentes", json=teacher)
    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_teacher(client):
    teacher = TeacherFactory.create_batch(2)
    response = client.post("/docentes", json=teacher)

    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_teacher(client):
    teacher = TeacherFactory.create_batch(2, matric=123456)
    response = client.post("/docentes", json=teacher)
    assert response.status_code == HTTPStatus.CONFLICT


def test_insert_teacher_existing_researcher(client, researcher):
    teacher = TeacherFactory.create_batch(1, nome=researcher[0]["name"])
    response = client.post("/docentes", json=teacher)

    assert response.status_code == HTTPStatus.CREATED
    from pprint import pprint

    pprint(client.get("/docentes").json)


def test_get_teacher_no_filter(client):
    teacher = TeacherFactory.create_batch(1)
    response = client.post("/docentes", json=teacher)
    teacher = TeacherFactory.create_batch(1)
    response = client.post("/docentes", json=teacher)

    response = client.get("/docentes")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 1


def test_get_teacher_no_filter(client):
    teacher = TeacherFactory.create_batch(1, year_charge=2020, semester=1)
    response = client.post("/docentes", json=teacher)
    teacher = TeacherFactory.create_batch(1, year_charge=2021)
    response = client.post("/docentes", json=teacher)

    response = client.get("/docentes?year=2020&semester=1")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json) == 1
