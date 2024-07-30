import pandas as pd
from ..dao import Connection
from ..models.teachers import ListTeachers, ListRole

adm_database = Connection()


def ufmg_researcher_insert(ListTeachers: ListTeachers):

    script_sql = """
        DELETE FROM UFMG.researcher
        WHERE semester = %s;
        """
    year = ListTeachers.list_teachers[0].year_charge
    semester = ListTeachers.list_teachers[0].semester
    adm_database.exec(script_sql, [f"{year}.{semester}"])

    parameters = list()

    for teacher in ListTeachers.list_teachers:
        script_sql = """
            SELECT researcher_id FROM researcher
            WHERE ts_rank(to_tsvector(unaccent(LOWER(name))), websearch_to_tsquery(%s)) > 0.04
            LIMIT 1;
            """

        researcher_id = adm_database.select(script_sql, [teacher.nome])
        if researcher_id:
            researcher_id = researcher_id[0][0]

        # fmt: off
        parameters.append((
            researcher_id if researcher_id else None, teacher.matric, teacher.inscUFMG,
            teacher.nome, teacher.genero, teacher.situacao, teacher.rt,
            teacher.clas, teacher.cargo, teacher.classe,
            teacher.ref, teacher.titulacao, teacher.entradaNaUFMG,
            teacher.progressao, f"{year}.{semester}"
        ))
        # fmt: on

    script_sql = """
        INSERT INTO UFMG.researcher
        (researcher_id, matric, inscUFMG, nome, genero, situacao, rt, clas, 
        cargo, classe, ref, titulacao, entradaNaUFMG, progressao, semester) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    adm_database.execmany(script_sql, parameters)


def reacher_basic_query(year, semester):
    parameters = list()
    if year or semester:
        parameters.append(f"{year}.{semester}")
        filter_semester = """
            WHERE semester = %s
            """
    else:
        filter_semester = """
            WHERE semester = (SELECT MAX(semester) FROM UFMG.researcher)
            """

    script_sql = f"""
        SELECT 
            id, researcher_id, matric, inscUFMG, nome, genero, situacao, rt, 
            clas, cargo, classe, ref, titulacao, entradaNaUFMG,
            progressao, semester
        FROM
            UFMG.researcher
        {filter_semester}
        """

    registry = adm_database.select(script_sql, parameters)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "id",
            "researcher_id",
            "matric",
            "inscUFMG",
            "nome",
            "genero",
            "situacao",
            "rt",
            "clas",
            "cargo",
            "classe",
            "ref",
            "titulacao",
            "entradaNaUFMG",
            "progressao",
            "semester",
        ],
    )
    return data_frame.to_dict(orient="records")


def teacher_query_semester():
    script_sql = """
    SELECT
        SUBSTRING(semester, 1, 4) AS year,
        SUBSTRING(semester, 6, 1) AS semester
    FROM
        ufmg.researcher
    GROUP BY semester;
    """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(registry, columns=["year", "semester"])

    return data_frame.to_dict(orient="records")


def teacher_insert_role(ListRole: ListRole):
    parameters = list()
    for role in ListRole.list_roles:
        parameters.append((
            role.role, role.researcher_id
        ))

    script_sql = """
        INSERT INTO researcher_role (role, researcher_id)
        VALUES (%s, %s)
        """

    adm_database.exec(script_sql, parameters)
