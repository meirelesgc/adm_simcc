# Para conseguir importar os modulos de projeto em tempo de execução desse script
from Model.Resercher import Researcher
import pandas as pd
import Dao.dbHandler as dbHandler
import sys

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


def Query(ID):
    sql = f"""
        SELECT 
            researcher_id, 
            name, 
            lattes_id, 
            institution_id 
        FROM 
            researcher 
        WHERE 
            institution_id = '{ID}'
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
