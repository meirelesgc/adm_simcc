import pandas as pd
from ..dao import Connection
from ..models.teachers import ListTeachers

adm_database = Connection()


def teacher_insert(ListTeachers: ListTeachers):
    script_sql = """
        DELETE FROM ufmg_teacher
        WHERE semester = %s;
        """
    year = ListTeachers.list_teachers[0].year_charge
    semester = ListTeachers.list_teachers[0].semester
    adm_database.exec(script_sql, [f"{year}.{semester}"])

    parameters = list()

    for teacher in ListTeachers.list_teachers:
        # fmt: off
        parameters.append((
            teacher.matric, teacher.inscUFMG,
            teacher.nome, teacher.genero, teacher.situacao, teacher.rt,
            teacher.clas, teacher.cargo, teacher.classe,
            teacher.ref, teacher.titulacao, teacher.entradaNaUFMG,
            teacher.progressao, f"{year}.{semester}"
        ))
        # fmt: on

    script_sql = """
        INSERT INTO ufmg_teacher
        (matric, inscUFMG, nome, genero, situacao, rt, clas, cargo, classe, ref,
        titulacao, entradaNaUFMG, progressao, semester) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
            WHERE semester = (SELECT MAX(semester) FROM ufmg_docente)
            """

    script_sql = f"""
        SELECT 
            matric, inscUFMG, nome, genero, situacao, rt, 
            clas, cargo, classe, ref, titulacao, entradaNaUFMG,
            progressao, semester
        FROM
            ufmg_teacher
        {filter_semester}
        """

    registry = adm_database.select(script_sql, parameters)

    data_frame = pd.DataFrame(
        registry,
        columns=[
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
