import pandas as pd

from ..dao import Connection
from ..models.student import GraduateProgramStudent, ListGraduateProgramStudent
from ..dao import dao_researcher


adm_database = Connection()


def student_insert(ListStudent: ListGraduateProgramStudent):
    SCRIPT_SQL = str()
    for student in ListStudent.student_list:
        main_data_base_id = dao_researcher.researcher_basic_query(
            lattes_id=student.lattes_id)  # fmt: skip
        if not main_data_base_id:
            SCRIPT_SQL += f"""
            INSERT INTO researcher (researcher_id, name, lattes_id, institution_id)
            VALUES ('{student.student_id}', '{student.name}', '{student.lattes_id}', '{student.institution_id}');
            """
        else:
            student.student_id = main_data_base_id[0]["researcher_id"]

        SCRIPT_SQL += f"""
        INSERT INTO graduate_program_student (graduate_program_id, researcher_id, year)
        VALUES ('{student.graduate_program_id}', '{student.student_id}', '{student.year}');
        """

    return adm_database.exec(SCRIPT_SQL)


def student_basic_query(graduate_program_id: str = None,
                        institution_id: str = None,
                        lattes_id: str = None):

    if lattes_id:
        filter_lattes_id = f"AND r.lattes_id = '{lattes_id}'"
    else:
        filter_lattes_id = str()

    if graduate_program_id:
        filter_graduate_program = (
            f"AND gps.graduate_program_id = '{graduate_program_id}'")
    else:
        filter_graduate_program = str()

    if institution_id:
        filter_institution = f"AND r.institution_id = '{institution_id}'"
    else:
        filter_institution = str()

    SCRIPT_SQL = f"""
        SELECT
            r.name,
            r.lattes_id,
            'DISCENTE' as type_
        FROM
            graduate_program_student gps
        LEFT JOIN researcher r ON
        r.researcher_id = gps.researcher_id
        WHERE 
            1 = 1
            {filter_graduate_program}
            {filter_institution}
            {filter_lattes_id};
    """
    registry = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(
        registry,
        columns=[
            "name",
            "lattes_id",
            "type_",
        ],
    )

    return data_frame.to_dict(orient="records")


def student_delete(student_id, graduate_program):
    SCRIPT_SQL = f"""
        DELETE FROM graduate_program_student gs
        USING researcher r
        WHERE gs.researcher_id = r.researcher_id
            AND r.lattes_id = '{student_id}'
            AND gs.graduate_program_id = '{graduate_program}';
        
        DELETE FROM researcher WHERE lattes_id = '{student_id}';
        """
    adm_database.exec(SCRIPT_SQL)


def student_update(student: GraduateProgramStudent):
    SCRIPT_SQL = f"""
        UPDATE researcher
        SET
            researcher_id = '{student.student_id}',
            name = '{student.name}',
            lattes_id = '{student.lattes_id}',
            institution_id = '{student.institution_id}'
        WHERE researcher_id = '{student.student_id}';
        """
    adm_database.exec(SCRIPT_SQL)
