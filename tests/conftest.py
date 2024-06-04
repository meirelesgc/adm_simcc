import os
import pytest
from testcontainers.postgres import PostgresContainer

from adm_simcc import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True,})  # fmt: skip

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


postgres = PostgresContainer("postgres:16-alpine", username="postgres")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["ADM_DATABASE"] = postgres.dbname
    os.environ["ADM_USER"] = postgres.username
    os.environ["ADM_HOST"] = postgres.get_container_host_ip()
    os.environ["ADM_PASSWORD"] = postgres.password
    os.environ["ADM_PORT"] = postgres.get_exposed_port(5432)
    os.environ["SIMCC_DATABASE"] = "simcc_"
    with open("scripts/database.sql", "r") as setup_file:
        script_sql = setup_file.read()
    postgres.exec(
        [
            "psql",
            "-U",
            os.environ["ADM_USER"],
            "-d",
            os.environ["ADM_DATABASE"],
            "-c",
            script_sql,
        ]
    )


# @pytest.fixture(scope="function", autouse=True)
# def setup_data_institution():
#     Connection.exec("DELETE FROM institution;")
