from tests.factories.research_group_factory import ResearchGroupFactory
from http import HTTPStatus


def test_insert_single_group(client, institution):
    group = ResearchGroupFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )
    response = client.post("/researchGroupRest/Insert", json=group)

    assert response.status_code == HTTPStatus.CREATED


def test_insert_some_group(client, institution):
    group = ResearchGroupFactory.create_batch(
        2, institution_id=institution[0]["institution_id"]
    )
    response = client.post("/researchGroupRest/Insert", json=group)

    assert response.status_code == HTTPStatus.CREATED


def test_violate_unique_constrain_group(client, institution):
    group = ResearchGroupFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )

    response = client.post("/researchGroupRest/Insert", json=group)
    response = client.post("/researchGroupRest/Insert", json=group)

    assert response.status_code == HTTPStatus.CONFLICT


def test_query_group_by_institution(client, research_group):
    institution_id = research_group[0]["institution_id"]
    endpoint = f"/researchGroupRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)

    assert len(response.json) == 2


def test_query_group_by_id(client, research_group):
    institution_id = research_group[0]["institution_id"]
    endpoint = f"/researchGroupRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)

    research_group_id = response.json[0]["research_group_id"]
    endpoint = f"/researchGroupRest/Query?research_group_id={research_group_id}"
    response = client.get(endpoint)

    assert len(response.json) == 1


def test_query_group_by_researcher(client, researcher, research_group):
    researcher_id = researcher[0]["researcher_id"]
    endpoint = f"/researchGroupRest/Query?researcher_id={researcher_id}"
    response = client.get(endpoint)

    assert len(response.json) == 2


def test_delete_group_by_institution(client, research_group):
    endpoint = f"/researchGroupRest/Delete?institution_id={research_group[0]['institution_id']}"
    response = client.delete(endpoint)

    assert response.status_code == HTTPStatus.NO_CONTENT

    institution_id = research_group[0]["institution_id"]
    endpoint = f"/researchGroupRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)

    assert len(response.json) == 0


def test_delete_group_by_id(client, research_group):
    institution_id = research_group[0]["institution_id"]
    endpoint = f"/researchGroupRest/Query?institution_id={institution_id}"
    response = client.get(endpoint)

    research_group_id = response.json[0]["research_group_id"]
    endpoint = f"/researchGroupRest/Delete?research_group_id={research_group_id}"
    response = client.delete(endpoint)
    assert response.status_code == HTTPStatus.NO_CONTENT

    endpoint = f"/researchGroupRest/Query?research_group_id={research_group_id}"
    response = client.get(endpoint)

    assert len(response.json) == 0


## Testes para Update não escritos
