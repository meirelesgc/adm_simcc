from tests.factories.researcher_factory import ResearcherFactory, SubsidiesFactory
from http import HTTPStatus


def test_insert_single_researcher(client, institution):
    researcher = ResearcherFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )

    response = client.post("/ResearcherRest/Insert", json=researcher)

    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_researchers(client, institution):
    researcher = ResearcherFactory.create_batch(
        3, institution_id=institution[0]["institution_id"]
    )

    response = client.post("/ResearcherRest/Insert", json=researcher)

    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_constrain_researcher(client, institution):
    researcher = ResearcherFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )

    response = client.post("/ResearcherRest/Insert", json=researcher)
    response = client.post("/ResearcherRest/Insert", json=researcher)

    assert response.status_code == HTTPStatus.CONFLICT


def test_query_researcher_by_name(client, researcher):
    endpoint = f"/ResearcherRest/Query?name={researcher[1]['name']}"
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json[0] == researcher[1]


def test_query_researcher_by_institution_id(client, researcher):
    endpoint = f"/ResearcherRest/Query?institution_id={researcher[2]['institution_id']}"
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert researcher[2] in response.json


def test_query_researcher_by_lattes_id(client, researcher):
    endpoint = f"/ResearcherRest/Query?lattes_id={researcher[2]['lattes_id']}"
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json[0] == researcher[2]


def test_query_researcher_with_limit(client, researcher):
    endpoint = f"/ResearcherRest/Query?institution_id={researcher[0]['institution_id']}&count=1"

    response = client.get(endpoint)
    count = len(response.json)

    assert response.status_code == HTTPStatus.OK
    assert count == 1


def test_delete_researcher(client, researcher):
    endpoint = f"/ResearcherRest/Delete?researcher_id={researcher[2]['researcher_id']}"
    response = client.delete(endpoint, json=researcher)

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_count_researchers_no_filters(client, researcher):
    endpoint = f"/ResearcherRest/Query/Count"
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json == 3


def test_count_researchers_with_filters(client, researcher):
    endpoint = f"/ResearcherRest/Query/Count?institution_id={researcher[2]['institution_id']}"  # fmt: skip
    response = client.get(endpoint)

    assert response.status_code == HTTPStatus.OK
    assert response.json == 3


def test_insert_single_subsidie(client, researcher):
    subsidie = SubsidiesFactory.create_batch(1, id_lattes=researcher[2]["lattes_id"])

    response = client.post("/ResearcherRest/InsertGrant", json=subsidie)

    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_subsidie(client, researcher):
    subsidie = SubsidiesFactory.create_batch(3, id_lattes=researcher[2]["lattes_id"])

    response = client.post("/ResearcherRest/InsertGrant", json=subsidie)

    assert response.status_code == HTTPStatus.CREATED


def test_query_subsidies_no_filters(client, researcher):
    subsidie = SubsidiesFactory.create_batch(1, id_lattes=researcher[2]["lattes_id"])
    response = client.post("/ResearcherRest/InsertGrant", json=subsidie)

    response = client.get("/ResearcherRest/Query/Subsidy")
    data = {
        "researcher_id": researcher[2]["researcher_id"],
        "name": researcher[2]["name"],
        "modality_code": subsidie[0]["cod_modalidade"],
        "modality_name": subsidie[0]["nome_modalidade"],
        "call_title": subsidie[0]["titulo_chamada"],
        "category_level_code": subsidie[0]["cod_categoria_nivel"],
        "funding_program_name": subsidie[0]["nome_programa_fomento"],
        "institute_name": subsidie[0]["nome_instituto"],
        "aid_quantity": str(subsidie[0]["quant_auxilio"]),
        "scholarship_quantity": str(subsidie[0]["quant_bolsa"]),
    }
    assert data in response.json


def test_query_subsidies_with_filters(client, researcher):
    subsidie = SubsidiesFactory.create_batch(1, id_lattes=researcher[2]["lattes_id"])
    response = client.post("/ResearcherRest/InsertGrant", json=subsidie)

    endpoint = f"/ResearcherRest/Query/Subsidy?institution_id={researcher[2]['institution_id']}"
    response = client.get(endpoint)

    data = {
        "researcher_id": researcher[2]["researcher_id"],
        "name": researcher[2]["name"],
        "modality_code": subsidie[0]["cod_modalidade"],
        "modality_name": subsidie[0]["nome_modalidade"],
        "call_title": subsidie[0]["titulo_chamada"],
        "category_level_code": subsidie[0]["cod_categoria_nivel"],
        "funding_program_name": subsidie[0]["nome_programa_fomento"],
        "institute_name": subsidie[0]["nome_instituto"],
        "aid_quantity": subsidie[0]["quant_auxilio"],
        "scholarship_quantity": subsidie[0]["quant_bolsa"],
    }
    assert data in response.json
