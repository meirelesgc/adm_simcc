# Para conseguir importar os modulos de projeto em tempo de execução desse script
from Model.GraduateProgram import GraduateProgram
import pandas as pd
import Dao.dbHandler as dbHandler
import sys

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
    sql = """
    SELECT * FROM graduate_program_researcher WHERE graduate_program_id = '{filter}'
""".format(
        filter=ID
    )
    return pd.DataFrame(
        dbHandler.db_select(sql),
        columns=[
            "graduate_program_id",
            "researcher_id",
            "year",
            "type_",
        ],
    )


def query_count():
    script_sql = "SELECT COUNT(*) FROM graduate_program_researcher;"

    return (dbHandler.db_select(script_sql=script_sql, rows=-1)[0])
