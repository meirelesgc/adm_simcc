import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.institution import ListInstitutions

adm_database = Connection()


def institution_insert(ListInstitutions: ListInstitutions):
    values_str = str()
    for institution in ListInstitutions.institution_list:
        values_str += f"""('{institution.institution_id}', '{institution.name}', '{institution.acronym}', '{institution.lattes_id}'),"""

    # Criação do script de insert.
    # Unifiquei em um unico comando para facilitar
    # o retorno da mensagem de erro
    script_sql = f"""
        INSERT INTO public.institution
        (institution_id, name, acronym, lattes_id)
        VALUES {values_str[:-1]};
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

    return data_frame.to_dict(orient="records")


def institution_basic_query(institution_id: UUID4):
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


def institution_query_name(institution_name: str):

    script_sql = f"""
    SELECT
        institution_id
    FROM
        institution as i
    WHERE
        similarity(unaccent(LOWER('{institution_name.replace("'", "''")}')), unaccent(LOWER(i.name))) > 0.4
    LIMIT 1;
    """

    registry = adm_database.select(script_sql)

    if registry:
        return registry[0][0]
    else:
        return None
