import os
import select
import pandas as pd
from pydantic import UUID4
from psycopg2 import Error

from ..dao import Connection
from ..models.researcher import ListResearchers

adm_database = Connection()
simcc_database = Connection(database=os.environ["SIMCC_DATABASE"])


def researcher_insert(ListResearchers: ListResearchers):

    values = str()
    for researcher in ListResearchers.researcher_list:
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
    try:
        adm_database.exec(script_sql)
    except Error as erro:
        raise erro


def researcher_delete(researcher_id: UUID4):
    script_sql = f"""
        BEGIN;

        DELETE FROM graduate_program_researcher
        WHERE researcher_id = '{researcher_id}';

        DELETE FROM researcher
        WHERE researcher_id = '{researcher_id}';

        COMMIT;
        """
    try:
        adm_database.exec(script_sql)
    except Error as erro:
        raise erro


def researcher_basic_query(institution_id: UUID4, researcher_name: str, rows: int):
    if institution_id:
        filter_institution = f"""
            AND r.institution_id = '{institution_id}'
            """
    else:
        filter_institution = str()
    if researcher_name:
        researcher_name = researcher_name.replace("'", "''")
        filter_name = f"""
            AND similarity(unaccent(LOWER('{researcher_name}')), unaccent(LOWER(r.name))) > 0.5
            """
    else:
        filter_name = str()
    if rows:
        filter_limit = f"""
            LIMIT {rows}
            """
    else:
        filter_limit = str()
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
            r.researcher_id NOT IN (
            SELECT
                researcher_id
            FROM
                graduate_program_researcher
            WHERE
                type_ = 'DISCENTE')
            {filter_institution}
            {filter_name}
            ORDER by created_at DESC
            {filter_limit}
        """

    registry = adm_database.select(script_sql=script_sql)

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
        WHERE 
            r.id NOT IN (
            SELECT
                researcher_id
            FROM
                graduate_program_researcher
            WHERE
                type_ = 'DISCENTE')
            {filter_institution}
        """

    registry = simcc_database.select(script_sql)

    data_frame_simcc = pd.DataFrame(registry, columns=["lattes_id", "last_update"])

    data_frame = pd.merge(data_frame, data_frame_simcc, on="lattes_id")

    return data_frame.to_dict(orient="records")


def researcher_count(institution_id: UUID4 = None):
    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE institution_id = '{institution_id}'"

    script_sql = f"SELECT COUNT(*) FROM researcher {filter_institution}"

    registry = adm_database.select(script_sql)

    # psycopg2 retorna uma lista de truplas,
    # quero apenas o primeiro valor da primeira lista
    return registry[0][0]
