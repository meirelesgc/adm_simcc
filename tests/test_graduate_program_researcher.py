from http import HTTPStatus


def test_insert_single_graduate_program_researcher(
    client, researcher, graduate_program
):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_graduate_program_researcher(client, researcher, graduate_program):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        },
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[1]["researcher_id"],
            "year": 0000,
            "type_": "PERMANENTE",
        },
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_constrain_graduate_program_researcher(
    client, researcher, graduate_program
):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    endpoint = "/GraduateProgramResearcherRest/Insert"
    response = client.post(endpoint, json=gp_researcher)
    response = client.post(endpoint, json=gp_researcher)
    assert response.status_code == HTTPStatus.CONFLICT


def test_delete_graduate_program_researcher(client, researcher, graduate_program):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)

    del_researcher = [
        {
            "lattes_id": researcher[0]["lattes_id"],
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
        }
    ]
    response = client.delete(
        "/GraduateProgramResearcherRest/Delete", json=del_researcher
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_query_graduate_program_researcher_no_filter(
    client, researcher, graduate_program
):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    endpoint = f"/GraduateProgramResearcherRest/Query?graduate_program_id={graduate_program[0]['graduate_program_id']}"
    response = client.get(endpoint)

    assert gp_researcher in response.json


def test_query_graduate_program_researcher_no_filter(
    client, researcher, graduate_program
):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    endpoint = f"/GraduateProgramResearcherRest/Query?graduate_program_id={graduate_program[0]['graduate_program_id']}"
    response = client.get(endpoint)

    assert gp_researcher[0]["type_"] in response.json[0]["type_"]


def test_query_graduate_program_researcher_with_filter(
    client, researcher, graduate_program
):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    endpoint = f"/GraduateProgramResearcherRest/Query?graduate_program_id={graduate_program[0]['graduate_program_id']}&type=PERMANENTE"
    response = client.get(endpoint)

    assert not response.json


def test_query_count_graduate_program_researcher(client, researcher, graduate_program):
    gp_researcher = [
        {
            "graduate_program_id": graduate_program[0]["graduate_program_id"],
            "researcher_id": researcher[0]["researcher_id"],
            "year": 0000,
            "type_": "COLABORADOR",
        }
    ]
    response = client.post("/GraduateProgramResearcherRest/Insert", json=gp_researcher)
    endpoint = f"/GraduateProgramResearcherRest/Query/Count"
    response = client.get(endpoint)
    assert response.json == 1
