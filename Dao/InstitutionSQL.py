# Para conseguir importar os modulos de projeto em tempo de execução desse script
import sys

sys.path.append("../")

import Dao.dbHandler as dbHandler
import pandas as pd


def Insert(Institution):
    sql = f"""
        INSERT INTO institution (institution_id, name, acronym, lattes_id)
        VALUES ('{Institution.institution_id}', '{Institution.name}', '{Institution.acronym}', '{Institution.lattes_id}')
        """

    return dbHandler.db_script(sql)


def Query(ID):
    sql = f"""
        SELECT 
            institution_id, 
            name, 
            acronym, 
            lattes_id
	    FROM 
            institution 
        WHERE 
            institution_id = '{ID}'
        """

    return pd.DataFrame(
        dbHandler.db_select(sql),
        columns=["institution_id", "name", "acronym", "lattes_id"],
    )
