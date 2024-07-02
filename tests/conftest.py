import os
import pytest
from testcontainers.postgres import PostgresContainer
from adm_simcc import create_app


postgres = PostgresContainer("postgres:16-alpine")

with open("scripts/database.sql", "r") as setup_file:
    script_database = setup_file.read()


@pytest.fixture(scope="package", autouse=True)
def postgres_container(request):

    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["ADM_HOST"] = postgres.get_container_host_ip()
    os.environ["ADM_PORT"] = postgres.get_exposed_port(5432)
    os.environ["ADM_DATABASE"] = postgres.dbname
    os.environ["ADM_USER"] = postgres.username
    os.environ["ADM_PASSWORD"] = postgres.password
    postgres.exec(["psql", "-U", os.environ["ADM_USER"], "-d", os.environ["ADM_DATABASE"], "-c", script_database])  # fmt: skip


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app
    teardown_sql = """
        DROP SCHEMA public CASCADE; 
        CREATE SCHEMA public;
        """
    postgres.exec(["psql", "-U", os.environ["ADM_USER"], "-d", os.environ["ADM_DATABASE"], "-c", teardown_sql])  # fmt: skip
    postgres.exec(["psql", "-U", os.environ["ADM_USER"], "-d", os.environ["ADM_DATABASE"], "-c", script_database])  # fmt: skip


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def institution():
    from adm_simcc.dao import dao_institution
    from adm_simcc.models.institution import ListInstitutions

    institution_list = [
        {
            "institution_id": "685e7a0b-bbd1-4278-b7a3-721aa0f4e542",
            "name": "Universidade",
            "acronym": "UNI",
            "lattes_id": "000000000000",
        }
    ]

    institution_instance = ListInstitutions(institution_list=institution_list)
    dao_institution.institution_insert(institution_instance)
    return institution_list


@pytest.fixture()
def researcher(institution):
    from adm_simcc.dao.dao_researcher import researcher_insert
    from adm_simcc.models.researcher import ListResearchers

    researcher_list = [
        {
            "researcher_id": "750e8530-e29b-41d4-a716-446655450111",
            "name": "Perpétua",
            "lattes_id": "5678901234",
            "institution_id": institution[0]["institution_id"],
        },
        {
            "researcher_id": "450eb8e3-9b61-4e3d-a716-226655447777",
            "name": "Modesto Pires",
            "lattes_id": "0987654321",
            "institution_id": institution[0]["institution_id"],
        },
        {
            "researcher_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Padre Mariano",
            "lattes_id": "1234567890",
            "institution_id": institution[0]["institution_id"],
        },
    ]

    subsidies = {
        "subsidies": [
            {
                "category_level_code": None,
                "modality_code": None,
                "subsidy_id": None,
            }
        ]
    }

    for researcher in researcher_list:
        researcher.update(subsidies)

    researcher_instance = ListResearchers(researcher_list=researcher_list)
    researcher_insert(researcher_instance)
    return researcher_list


@pytest.fixture()
def graduate_program(institution):
    from adm_simcc.dao.dao_graduate_program import graduate_program_insert
    from adm_simcc.models.graduate_program import ListGraduateProgram

    graduate_program_list = [
        {
            "graduate_program_id": "62ecafdb-a614-415c-a2cc-d2484dde92ab",
            "code": "GP2024",
            "name": "Program Name",
            "area": "Science",
            "modality": "Full-time",
            "type": "PhD",
            "rating": "A",
            "institution_id": institution[0]["institution_id"],
            "city": "Salvador",
            "url_image": "http://example.com/image.jpg",
            "sigla": "UPA",
            "description": "This is a graduate program description.",
            "visible": False,
        }
    ]

    graduate_program_instance = ListGraduateProgram(
        graduate_program_list=graduate_program_list
    )
    graduate_program_insert(graduate_program_instance)
    return graduate_program_list


@pytest.fixture()
def another_graduate_program(institution):
    from adm_simcc.dao.dao_graduate_program import graduate_program_insert
    from adm_simcc.models.graduate_program import ListGraduateProgram

    graduate_program_list = [
        {
            "graduate_program_id": "9249927e-71dd-4f8c-a721-f26cd5d5c2fb",
            "code": "GP2025",
            "name": "Updated Program Name",
            "area": "Technology",
            "modality": "Part-time",
            "type": "Masters",
            "rating": "B",
            "institution_id": institution[0]["institution_id"],
            "city": "São Paulo",
            "url_image": "http://example.com/new_image.jpg",
            "sigla": "UPB",
            "description": "This is an updated graduate program description.",
            "visible": True,
        }
    ]

    graduate_program_instance = ListGraduateProgram(
        graduate_program_list=graduate_program_list
    )
    graduate_program_insert(graduate_program_instance)
    return graduate_program_list
