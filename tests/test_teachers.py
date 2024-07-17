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
