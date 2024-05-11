import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.researcher import Researcher

adm_database = Connection()


def researcher_insert(Researcher: Researcher):
    script_sql = f"""
        INSERT INTO researcher
        (researcher_id, name, lattes_id, institution_id)
        VALUES (
            '{Researcher.researcher_id}', 
            '{Researcher.name}', 
            '{Researcher.lattes_id}', 
            '{Researcher.institution_id}');
        """
    adm_database.exec(script_sql)


def researcher_delete(researcher_id: UUID4):
    script_sql = f"""
        DELETE FROM graduate_program_researcher 
        WHERE researcher_id = '{researcher_id}';
        
        DELETE FROM researcher 
        WHERE researcher_id = '{researcher_id}';
        """
    adm_database.exec(script_sql)


def researcher_basic_query(institution_id: UUID4):
    script_sql = f"""
        SELECT
            researcher_id,
            name,
            lattes_id,
            institution_id
        FROM
            researcher
        WHERE
            institution_id = '{institution_id}'
            AND researcher_id NOT IN (
                SELECT 
                    researcher_id 
                FROM 
                    graduate_program_researcher 
                WHERE 
                    type_ = 'DISCENTE')
        """

    registry = adm_database.select(script_sql=script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["researcher_id", "name", "lattes_id", "institution_id"],
    )
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
