from ..dao import Connection
from ..models.teachers import ListTeachers
from datetime import datetime

adm_database = Connection()


def teacher_insert(ListTeachers: ListTeachers):
    script_sql = """
        DELETE FROM UFMG.teacher 
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
            teacher.progressao, semester
        ))
        # fmt: on

    script_sql = """
        INSERT INTO UFMG.teacher 
        (matric, inscUFMG, nome, genero, situacao, rt, clas, cargo, classe, ref,
        titulacao, entradaNaUFMG, progressao, semester) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    adm_database.execmany(script_sql, parameters)


def reacher_basic_query(year, semester):

    if year or semester:
        parameters = [f"{year}.{semester}"]
        filter_semester = """
            WHERE 
            """
    script_sql = """
    SELECT 
        matric, inscUFMG, nome, genero, situacao, rt, clas, cargo, classe, ref,
        titulacao, entradaNaUFMG, progressao, semester
    FROM
        UFMG.teacher

    """
