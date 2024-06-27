from tests.factories.graduate_program_factory import GraduateProgramFactory
from http import HTTPStatus
from uuid import uuid4


def test_insert_single_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_graduate_programs(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        2, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_graduate_programs(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        2, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    assert response.status_code == HTTPStatus.CONFLICT


def test_query_single_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    endpoint = f"/GraduateProgramRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)
    expected_graduate_program = graduate_program[0]
    expected_graduate_program.update(
        {"qtd_colaborador": 0, "qtd_discente": 0, "qtd_permanente": 0}
    )
    assert expected_graduate_program in response.json


def test_query_graduate_programs(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        2, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    endpoint = f"/GraduateProgramRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)
    assert len(response.json) == 2


def test_update_visible_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    graduate_program_id = graduate_program[0]["graduate_program_id"]
    endpoint = f"/GraduateProgramRest/Update?graduate_program_id={graduate_program_id}"
    response = client.post(endpoint)
    assert response.status_code == HTTPStatus.OK

    endpoint = f"/GraduateProgramRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)
    assert response.json[0]["visible"] != graduate_program[0]["visible"]


def test_return_visible_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    graduate_program_id = graduate_program[0]["graduate_program_id"]
    endpoint = f"/GraduateProgramRest/Update?graduate_program_id={graduate_program_id}"
    response = client.post(endpoint)
    response = client.post(endpoint)
    assert response.status_code == HTTPStatus.OK
    endpoint = f"/GraduateProgramRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)
    assert response.json[0]["visible"] == graduate_program[0]["visible"]


def test_fix_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id, graduate_program_id=str(uuid4())
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    graduate_program[0]["description"] = "A palavra cabalistica"
    response = client.post("/GraduateProgramRest/Fix", json=graduate_program)
    assert response.status_code == HTTPStatus.OK
    endpoint = f"/GraduateProgramRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)
    expected_graduate_program = graduate_program[0]
    expected_graduate_program.update(
        {"qtd_colaborador": 0, "qtd_discente": 0, "qtd_permanente": 0}
    )
    assert expected_graduate_program in response.json


def test_delete_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id, graduate_program_id=str(uuid4())
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    endpoint = f"/GraduateProgramRest/Delete?graduate_program_id={graduate_program[0]['graduate_program_id']}"
    response = client.delete(endpoint)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_count_graduate_program(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id, graduate_program_id=str(uuid4())
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    endpoint = f"/GraduateProgramRest/Query/Count?institution_id={institution_id}"
    response = client.get(endpoint)
    assert response.json == 1


def test_count_graduate_program_no_filter(client, institution):
    institution_id = institution[0]["institution_id"]
    graduate_program = GraduateProgramFactory.create_batch(
        1, institution_id=institution_id, graduate_program_id=str(uuid4())
    )
    response = client.post("/GraduateProgramRest/Insert", json=graduate_program)
    endpoint = f"/GraduateProgramRest/Query/Count"
    response = client.get(endpoint)
    assert response.json == 1
