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
    script_sql = """
        INSERT INTO institution (institution_id, name, acronym, lattes_id)
        VALUES 
        ('685e7a0b-bbd1-4278-b7a3-721aa0f4e542', 'Universidade', 'UNI', '000000000000');
        """
    postgres.exec(["psql", "-U", os.environ["ADM_USER"], "-d", os.environ["ADM_DATABASE"], "-c", script_sql])  # fmt: skip
    return [
        {
            "institution_id": "685e7a0b-bbd1-4278-b7a3-721aa0f4e542",
            "name": "Universidade",
            "acronym": "UNI",
            "lattes_id": 000000000000,
        }
    ]


@pytest.fixture()
def researcher(institution):
    script_sql = f"""
        INSERT INTO researcher (researcher_id, name, lattes_id, institution_id)
        VALUES
        ('750e8530-e29b-41d4-a716-446655450111', 'Carol Brown', '5678901234', '{institution[0]['institution_id']}'),
        ('450eb8e3-9b61-4e3d-a716-226655447777', 'Bob Johnson', '0987654321', '{institution[0]['institution_id']}'),
        ('550e8400-e29b-41d4-a716-446655440000', 'Alice Smith', '1234567890', '{institution[0]['institution_id']}');
        """
    postgres.exec(["psql", "-U", os.environ["ADM_USER"], "-d", os.environ["ADM_DATABASE"], "-c", script_sql])  # fmt: skip
    return [
        {
            "researcher_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Alice Smith",
            "lattes_id": "1234567890",
            "institution_id": institution[0]["institution_id"],
            "subsidies": [
                {
                    "category_level_code": None,
                    "modality_code": None,
                    "subsidy_id": None,
                },
            ],
        },
        {
            "researcher_id": "450eb8e3-9b61-4e3d-a716-226655447777",
            "name": "Bob Johnson",
            "lattes_id": "0987654321",
            "institution_id": institution[0]["institution_id"],
            "subsidies": [
                {
                    "category_level_code": None,
                    "modality_code": None,
                    "subsidy_id": None,
                },
            ],
        },
        {
            "researcher_id": "750e8530-e29b-41d4-a716-446655450111",
            "name": "Carol Brown",
            "lattes_id": "5678901234",
            "institution_id": institution[0]["institution_id"],
            "subsidies": [
                {
                    "category_level_code": None,
                    "modality_code": None,
                    "subsidy_id": None,
                },
            ],
        },
    ]
