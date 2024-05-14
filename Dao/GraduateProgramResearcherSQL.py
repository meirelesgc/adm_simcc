# Para conseguir importar os modulos de projeto em tempo de execução desse script
import sys

import pandas as pd

import Dao.dbHandler as dbHandler
from Model.GraduateProgramResearcher import GraduateProgramResearcher

sys.path.append("../")


def insert(researcher: GraduateProgramResearcher):
    script_sql = f"""
    INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
    VALUES (
        '{researcher.graduate_program_id}',
        '{researcher.researcher_id}',
        '{researcher.year}',
        '{researcher.type_}')
    """
    return dbHandler.db_script(script_sql)


def query(graduate_program_id, type_: str = None):

    if type_:
        type_filter = f"AND type = '{type_}'"
    else:
        type_filter = "AND type_ IN ('PERMANENTE', 'COLABORADOR')"

    script_sql = f"""
        SELECT
            r.name,
            r.lattes_id,
            gpr.type_,
            gpr.created_at
        FROM 
            graduate_program_researcher gpr
        JOIN researcher r ON 
        r.researcher_id = gpr.researcher_id
        WHERE 
            gpr.graduate_program_id = '{graduate_program_id}'
            {type_filter}
        ORDER BY gpr.created_at
        """

    registry = dbHandler.db_select(script_sql)


    print(script_sql)
    data_frame = pd.DataFrame(
        registry,
        columns=[
            "name",
            "lattes_id",
            "type_",
            "created_at"
        ],
    )

    return data_frame.to_dict(orient="records")


def query_count(institution_id):
    script_sql = f"""
    SELECT 
        COUNT(*)
    FROM 
        graduate_program_researcher gpr
    JOIN graduate_program gp ON
    gp.graduate_program_id = gpr.graduate_program_id
    WHERE institution_id = '{institution_id}';
    """

    return dbHandler.db_select(script_sql=script_sql, rows=-1)[0]


def delete(researcher_id, graduate_program_id):
    dbHandler.db_script(
        f"""DELETE FROM 
            graduate_program_researcher 
        WHERE researcher_id = (SELECT researcher_id FROM researcher WHERE lattes_id = '{researcher_id}') 
        AND graduate_program_id = '{graduate_program_id}';"""
    )
    return "Delete concluido"
