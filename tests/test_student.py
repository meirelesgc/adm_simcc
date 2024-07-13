from tests.factories.student_factory import StudentFactory
from http import HTTPStatus


def test_insert_single_student(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )

    response = client.post("/studentRest/insert", json=student)
    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_student(client, graduate_program):
    student = StudentFactory.create_batch(
        2,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )

    response = client.post("/studentRest/insert", json=student)
    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_student(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )

    response = client.post("/studentRest/insert", json=student)
    response = client.post("/studentRest/insert", json=student)

    assert response.status_code == HTTPStatus.CONFLICT


def test_update_student(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )

    response = client.post("/studentRest/insert", json=student)
    student[0]["year"] = 2030
    response = client.post("/studentRest/update", json=student)

    assert response.status_code == HTTPStatus.OK


def test_query_student_no_filter(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )
    response = client.post("/studentRest/insert", json=student)
    response = client.get("/studentRest/query")

    data = {
        "name": student[0]["name"],
        "lattes_id": student[0]["lattes_id"],
        "type_": "DISCENTE",
    }
    assert data in response.json


def test_query_student_institution_filter(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )
    response = client.post("/studentRest/insert", json=student)
    endpoint = f"/studentRest/query?institution_id={graduate_program[0]["institution_id"]}"
    response = client.get(endpoint)

    data = {
        "name": student[0]["name"],
        "lattes_id": student[0]["lattes_id"],
        "type_": "DISCENTE",
    }
    assert data in response.json

def test_query_student_graduate_program_filter(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )
    response = client.post("/studentRest/insert", json=student)
    endpoint = f"/studentRest/query?graduate_program_id={graduate_program[0]["graduate_program_id"]}"
    response = client.get(endpoint)

    data = {
        "name": student[0]["name"],
        "lattes_id": student[0]["lattes_id"],
        "type_": "DISCENTE",
    }
    assert data in response.json

def test_delete_student(client, graduate_program):
    student = StudentFactory.create_batch(
        1,
        institution_id=graduate_program[0]["institution_id"],
        graduate_program_id=graduate_program[0]["graduate_program_id"],
    )
    response = client.post("/studentRest/insert", json=student)
    response = client.delete("/studentRest/delete", json=student)

    assert response.status_code == HTTPStatus.NO_CONTENT
    
