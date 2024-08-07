import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.graduate_program_resarcher import ListResearcher

adm_database = Connection()


def graduate_program_researcher_insert(
    ListResearcher: ListResearcher,
):
    parameters = list()

    # fmt: 0ff
    for researcher in ListResearcher.researcher_list:
        parameters.append(
            (
                researcher.graduate_program_id,
                researcher.researcher_id,
                researcher.year,
                researcher.type_,
            )
        )
    # fmt: on

    script_sql = f"""
        INSERT INTO graduate_program_researcher(
        graduate_program_id, researcher_id, year, type_)
        VALUES (%s, %s, %s, %s);
        """
    adm_database.execmany(script_sql, parameters)


def graduate_program_researcher_delete(
    researcher_id: UUID4, graduate_program_id: UUID4
):
    parameters = [researcher_id, graduate_program_id]
    script_sql = f"""
        DELETE FROM graduate_program_researcher
        WHERE
            researcher_id = (
                SELECT researcher_id
                FROM researcher
                WHERE lattes_id = %s)
            AND graduate_program_id = %s;"""
    adm_database.exec(script_sql, parameters)


def graduate_program_researcher_count(
    institution_id: UUID4 = None, graduate_program_id: UUID4 = None
):
    parameters = list()

    filter_institution = str()
    if institution_id:
        filter_institution = f"""
            WHERE
                graduate_program_id IN (
                    SELECT
                        graduate_program_id
                    FROM
                        graduate_program
                    WHERE
                        institution_id = %s)"""
        parameters.append(institution_id)

    if graduate_program_id:
        filter_graduate_program = f"""
            WHERE
                graduate_program_id = %s"""
        parameters.append(graduate_program_id)
    else:
        filter_graduate_program = str()

    script_sql = f"""
        SELECT
            COUNT(*)
        FROM
            graduate_program_researcher
        {filter_institution}
        {filter_graduate_program};
        """

    registry = adm_database.select(script_sql, parameters)

    return registry[0][0]


def graduate_program_researcher_basic_query(
    graduate_program_id: UUID4, type_: str = None
):
    parameters = [graduate_program_id]

    if type_:
        type_filter = f"AND type_ = %s"
        parameters.append(type_)
    else:
        type_filter = "AND type_ IN ('PERMANENTE', 'COLABORADOR')"

    script_sql = f"""
        SELECT
            r.name, r.lattes_id,
            gpr.type_, gpr.created_at
        FROM
            graduate_program_researcher gpr
            JOIN researcher r ON r.researcher_id = gpr.researcher_id
        WHERE
            gpr.graduate_program_id = %s
            {type_filter}
        ORDER BY 
            gpr.created_at DESC
        """

    registry = adm_database.select(script_sql, parameters)

    data_frame = pd.DataFrame(
        registry,
        columns=["name", "lattes_id", "type_", "created_at"],
    )

    return data_frame.to_dict(orient="records")
