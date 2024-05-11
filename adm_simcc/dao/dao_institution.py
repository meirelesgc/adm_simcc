import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.institution import Institution

adm_database = Connection()


def institution_insert(Institution: Institution):
    script_sql = f"""
        INSERT INTO institution
        (institution_id, name, acronym, lattes_id)
        VALUES (
            '{Institution.institution_id}',
            '{Institution.name}',
            '{Institution.acronym}',
            '{Institution.lattes_id}')
        """
    adm_database.exec(script_sql)


def institution_full_query(institution_id: UUID4 = None):
    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE i.institution_id = '{institution_id}'"

    script_sql = f"""
        SELECT
            i.name AS name,
            i.institution_id,
            COUNT(DISTINCT gp.graduate_program_id) AS count_gp,
            COUNT(gpr.researcher_id) AS count_gpr,
            COUNT(DISTINCT r.researcher_id) as count_r
        FROM
            institution i
        LEFT JOIN graduate_program gp
            ON gp.institution_id = i.institution_id
        LEFT JOIN graduate_program_researcher gpr
            ON gpr.graduate_program_id = gp.graduate_program_id
        LEFT JOIN researcher r
            ON r.institution_id = i.institution_id
        {filter_institution}
        GROUP BY
            i.institution_id, i.name;
        """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["name", "institution_id", "count_gp", "count_gpr", "count_r"],
    )


def institution_basic_query(institution_id: UUID4 = None):
    script_sql = f"""
        SELECT
            institution_id,
            name,
            acronym,
            lattes_id
	    FROM
            institution
        WHERE
            institution_id = '{institution_id}'
        """

    registry = adm_database.select(script_sql=script_sql)

    data_frame = pd.DataFrame(
        registry, columns=["institution_id", "name", "acronym", "lattes_id"]
    )

    # to_dict retorna uma lista, e eu so quero o primeiro valor
    return data_frame.to_dict(orient="records")[0]
