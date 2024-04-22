# Para conseguir importar os modulos de projeto em tempo de execução desse script
import sys

import pandas as pd

import Dao.dbHandler as dbHandler
from Model.GraduateProgram import GraduateProgram

sys.path.append("../")


def insert(GraduateProgram):
    sql = """
    INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
    VALUES
        ('{graduate_program_id}', '{researcher_id}', '{year}', '{type_}')
    """.format(
        graduate_program_id=GraduateProgram.graduate_program_id,
        researcher_id=GraduateProgram.researcher_id,
        year=GraduateProgram.year,
        type_=GraduateProgram.type_,
    )

    return dbHandler.db_script(sql)


def query(ID):
    sql = f"""
        SELECT 
            r.name,
            r.lattes_id,
            gpr.type_
        FROM 
            graduate_program_researcher gpr
        JOIN researcher r ON 
        r.researcher_id = gpr.researcher_id
        WHERE 
            graduate_program_id = '{ID}'
    """
    return pd.DataFrame(
        dbHandler.db_select(sql),
        columns=[
            "name",
            "lattes_id",
            "type_",
        ],
    )


def query_count():
    script_sql = "SELECT COUNT(*) FROM graduate_program_researcher;"

    return dbHandler.db_select(script_sql=script_sql, rows=-1)[0]


def delete(researcher_id, graduate_program_id):
    dbHandler.db_script(
        f"DELETE FROM graduate_program_researcher WHERE researcher_id = '{researcher_id}' AND graduate_program_id = '{graduate_program_id}';"
    )
    return "Delete concluido"
