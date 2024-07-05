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
    from tests.factories.institution_factory import InstitutionFactory

    institution_list = InstitutionFactory.create_batch(1)

    institution_instance = ListInstitutions(institution_list=institution_list)
    dao_institution.institution_insert(institution_instance)
    return institution_list


@pytest.fixture()
def researcher(institution):
    from adm_simcc.dao.dao_researcher import researcher_insert
    from adm_simcc.models.researcher import ListResearchers
    from tests.factories.researcher_factory import FullResearcherFactory

    researcher_list = FullResearcherFactory.create_batch(
        3, institution_id=institution[0]["institution_id"]
    )

    researcher_instance = ListResearchers(researcher_list=researcher_list)
    researcher_insert(researcher_instance)
    return researcher_list


@pytest.fixture()
def graduate_program(institution):
    from adm_simcc.dao.dao_graduate_program import graduate_program_insert
    from adm_simcc.models.graduate_program import ListGraduateProgram
    from tests.factories.graduate_program_factory import GraduateProgramFactory

    graduate_program_list = GraduateProgramFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )

    graduate_program_instance = ListGraduateProgram(
        graduate_program_list=graduate_program_list
    )
    graduate_program_insert(graduate_program_instance)
    return graduate_program_list


@pytest.fixture()
def another_graduate_program(institution):
    from adm_simcc.dao.dao_graduate_program import graduate_program_insert
    from adm_simcc.models.graduate_program import ListGraduateProgram
    from tests.factories.graduate_program_factory import GraduateProgramFactory

    graduate_program_list = GraduateProgramFactory.create_batch(
        1, institution_id=institution[0]["institution_id"]
    )

    graduate_program_instance = ListGraduateProgram(
        graduate_program_list=graduate_program_list
    )
    graduate_program_insert(graduate_program_instance)
    return graduate_program_list


@pytest.fixture()
def research_group(institution, researcher):
    from adm_simcc.dao.dao_researcher_group import research_group_insert
    from adm_simcc.models.researcher_group import ListResearcherGroup
    from tests.factories.research_group_factory import ResearchGroupFactory

    group_list = ResearchGroupFactory.create_batch(
        2,
        institution_id=institution[0]["institution_id"],
        nome_lider=researcher[0]["name"],
    )

    group_instance = ListResearcherGroup(researcher_groups_list=group_list)
    research_group_insert(group_instance)
    return group_list
