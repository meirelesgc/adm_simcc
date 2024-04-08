# Para conseguir importar os modulos de projeto em tempo de execução desse script
import pandas as pd
import Dao.dbHandler as dbHandler
import sys

sys.path.append("../")


def Insert(Institution):
    sql = f"""
        INSERT INTO institution (institution_id, name, acronym, lattes_id)
        VALUES ('{Institution.institution_id}', '{Institution.name}', '{Institution.acronym}', '{Institution.lattes_id}')
        """

    return dbHandler.db_script(sql)


def query_table(ID):
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


def query_count():
    script_sql = "SELECT COUNT(*) FROM institution;"

    return (dbHandler.db_select(script_sql=script_sql, rows=-1)[0])
