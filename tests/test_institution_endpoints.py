from http import HTTPStatus
from tests.factories.institution_factory import InstitutionFactory
from adm_simcc.dao import Connection


def test_insert_single_institution(client):
    db = Connection()
    breakpoint()
    assert 1 == 1
    # institutions_list = InstitutionFactory.create_batch(3)
    # response = client.post("/InstitutionRest/Insert", json=institutions_list)
    # script_sql = "SELECT COUNT(*) FROM institutions;"
    # institutions_count = db.select(script_sql=script_sql)
    # assert response.status_code == HTTPStatus.CREATED
    # assert institutions_count[0][0] == 3
