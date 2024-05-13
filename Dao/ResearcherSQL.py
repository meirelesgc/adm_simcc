# Para conseguir importar os modulos de projeto em tempo de execução desse script
import sys

import pandas as pd

import Dao.dbHandler as dbHandler
from Model.Resercher import Researcher

sys.path.append("../")


def Insert(Researcher):
    sql = """
      INSERT INTO researcher (researcher_id, name, lattes_id, institution_id)
      VALUES ('{researcher_id}', '{name}', '{lattes_id}', '{institution_id}')
   """.format(
        researcher_id=Researcher.researcher_id,
        name=Researcher.name,
        lattes_id=Researcher.lattes_id,
        institution_id=Researcher.institution_id,
    )

    return dbHandler.db_script(sql)


def Query(institution_id):
    sql = f"""
        SELECT DISTINCT
            r.researcher_id, 
            r.name,
            r.lattes_id,
            r.institution_id
        FROM
            researcher r
        WHERE 
            r.institution_id = '{institution_id}'
            AND r.researcher_id NOT IN (
                SELECT 
                    researcher_id
                FROM
                    graduate_program_researcher
                WHERE
                    type_ = 'DISCENTE') 
        """

    return pd.DataFrame(
        dbHandler.db_select(sql),
        columns=["researcher_id", "name", "lattes_id", "institution_id"],
    )


def Delete(ID):
    sql = """
    DELETE FROM graduate_program_researcher WHERE researcher_id = '{filter}';
             DELETE FROM researcher WHERE researcher_id = '{filter}';
""".format(
        filter=ID
    )
    dbHandler.db_script(script_sql=sql)
    return "OK"


def query_count(institution_id):
    filter = str()
    if institution_id:
        filter = f"WHERE institution_id = '{institution_id}'"

    script_sql = f"SELECT COUNT(*) FROM researcher {filter};"

    return dbHandler.db_select(script_sql=script_sql, rows=-1)[0]


def QueryByName(researcher_name):
    sql = f"""
    SELECT 
        researcher_id
    FROM 
        researcher as r
    WHERE 
        similarity(unaccent(LOWER('{researcher_name.replace("'", "''")}')), unaccent(LOWER(r.name))) > 0.8
    LIMIT 1;
    """

    result = dbHandler.db_select(sql)
    if result:
        return result[0][0]
    else:
        return None
