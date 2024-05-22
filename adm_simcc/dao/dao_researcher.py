import os
import pandas as pd

from pydantic import UUID4

from ..dao import Connection
from ..models.researcher import ListResearchers

adm_database = Connection()
simcc_database = Connection(database=os.environ["SIMCC_DATABASE"])


def researcher_insert(ListResearchers: ListResearchers):

    values = str()

    for researcher in ListResearchers.researcher_list:
        if researcher_basic_query(lattes_id=researcher.lattes_id):
            return 400
        values += f"""(
            '{researcher.researcher_id}',
            '{researcher.name}',
            '{researcher.lattes_id}',
            '{researcher.institution_id}'),"""

    # Criação do script de insert.
    # Unifiquei em um unico comando para facilitar
    # o retorno da mensagem de erro
    script_sql = f"""
        INSERT INTO researcher
        (researcher_id, name, lattes_id, institution_id)
        VALUES {values[:-1]};
        """
    adm_database.exec(script_sql)
    return 200


def researcher_delete(researcher_id: UUID4):
    script_sql = f"""
        DELETE FROM graduate_program_researcher
        WHERE researcher_id = '{researcher_id}';

        DELETE FROM researcher
        WHERE researcher_id = '{researcher_id}';
        """
    adm_database.exec(script_sql)


def researcher_basic_query(
    institution_id: UUID4 = None,
    researcher_name: str = None,
    rows: int = None,
    lattes_id: str = None,
):
    filter_name = filter_limit = filter_institution = filter_lattes_id = str()
    if institution_id:
        filter_institution = f"""
            AND r.institution_id = '{institution_id}'
            """
    if researcher_name:
        researcher_name = researcher_name.replace("'", "''")
        filter_name = f"""
            AND name ILIKE '{researcher_name}%'
            """
    if rows:
        filter_limit = f"LIMIT {rows}"

    if lattes_id:
        filter_lattes_id = f"AND lattes_id = '{lattes_id}'"

    script_sql = f"""
        SELECT DISTINCT
            r.researcher_id,
            r.name,
            r.lattes_id,
            r.institution_id,
            r.created_at
        FROM
            researcher r
        WHERE
            r.researcher_id NOT IN (SELECT researcher_id FROM public.graduate_program_student)
            {filter_institution}
            {filter_name}
            {filter_lattes_id}
            ORDER by created_at DESC
            {filter_limit}
        """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["researcher_id", "name", "lattes_id", "institution_id", "created_at"],
    )
    script_sql = f"""
        SELECT
            r.lattes_id,
            r.last_update
        FROM
            researcher r
        """

    registry = simcc_database.select(script_sql=script_sql)
    data_frame_simcc = pd.DataFrame(registry, columns=["lattes_id", "last_update"])
    data_frame = pd.merge(data_frame, data_frame_simcc, how="left", on="lattes_id")

    return data_frame.fillna("Não esta atualizado").to_dict(orient="records")


def researcher_count(institution_id: UUID4 = None):
    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE institution_id = '{institution_id}'"

    script_sql = f"SELECT COUNT(*) FROM researcher {filter_institution}"

    registry = adm_database.select(script_sql)

    # psycopg2 retorna uma lista de truplas,
    # quero apenas o primeiro valor da primeira lista
    return registry[0][0]


def researcher_query_name(researcher_name: str):
    script_sql = f"""
    SELECT
        researcher_id
    FROM
        researcher as r
    WHERE
        similarity(unaccent(LOWER('{researcher_name.replace("'", "''")}')), unaccent(LOWER(r.name))) > 0.8
    LIMIT 1;
    """

    registry = adm_database.select(script_sql)
    if registry:
        return registry[0][0]
    else:
        return None
