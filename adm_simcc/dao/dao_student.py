import pandas as pd
from pydantic import UUID4
from psycopg2 import Error

from ..dao import Connection
from ..models.student import Student, ListStudent

adm_database = Connection()


def student_insert(ListStudent: ListStudent):
    base_values = graduate_program_values = str()
    for student in ListStudent.student_list:
        base_values += f"""(
            '{student.student_id}',
            '{student.name}',
            '{student.lattes_id}',
            '{student.institution_id}'),"""

        graduate_program_values += f"""(
            '{student.graduate_program_id}',
            '{student.student_id}',
            '{student.year}',
            'DISCENTE'),"""

    script_sql = f"""
        INSERT INTO researcher (researcher_id, name, lattes_id, institution_id)
        VALUES {base_values[:-1]};

        INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
        VALUES {graduate_program_values[:-1]};
        """

    adm_database.exec(script_sql)


def student_basic_query(graduate_program_id: str = None, institution_id: str = None):
    if graduate_program_id:
        filter_graduate_program = (
            f"AND gpr.graduate_program_id = '{graduate_program_id}'"
        )
    else:
        filter_graduate_program = str()
    if institution_id:
        filter_institution = f"AND r.institution_id = '{institution_id}'"
    else:
        filter_institution = str()

    script_sql = f"""
        SELECT
            r.name,
            r.lattes_id,
            gpr.type_
        FROM
            graduate_program_researcher gpr
        JOIN researcher r ON
        r.researcher_id = gpr.researcher_id
        WHERE
            gpr.type_ = 'DISCENTE'
            {filter_graduate_program}
            {filter_institution}

    """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "name",
            "lattes_id",
            "type_",
        ],
    )

    return data_frame.to_dict(orient="records")


def student_delete(student_id):
    script_sql = f"""
        DELETE FROM graduate_program_researcher WHERE researcher_id = '{student_id}';
        DELETE FROM researcher WHERE researcher_id = '{student_id}';
        """
    adm_database.exec(script_sql)


def student_update(student: Student):
    script_sql = f"""
        UPDATE public.researcher
        SET
            researcher_id = '{student.student_id}',
            name = '{student.name}',
            lattes_id = '{student.lattes_id}',
            institution_id = '{student.institution_id}'
        WHERE researcher_id = '{student.student_id}';
        """
    adm_database.exec(script_sql)
