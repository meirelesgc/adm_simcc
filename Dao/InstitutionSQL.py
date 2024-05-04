# Para conseguir importar os modulos de projeto em tempo de execução desse script
import pandas as pd
import Dao.dbHandler as dbHandler
import sys

sys.path.append("../")


def Insert(Institution):
    sql = f"""
        INSERT INTO institution (institution_id, name, acronym, lattes_id)
        VALUES ({Institution.institution_id}', '{Institution.name}', '{Institution.acronym}', '{Institution.lattes_id}')
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


def query_count(institution_id: str = None):

    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE i.institution_id = '{institution_id}'"

    script_sql = f"""
        SELECT 
            i.name AS name,
            i.institution_id,
            COUNT(DISTINCT gp.graduate_program_id) AS count_gp,
            COUNT(gpr.researcher_id) AS count_gpr
        FROM 
            institution i
        LEFT JOIN graduate_program gp
            ON gp.institution_id = i.institution_id
        LEFT JOIN graduate_program_researcher gpr
            ON gpr.graduate_program_id = gp.graduate_program_id
        {filter_institution}
        GROUP BY
            i.institution_id, i.name;
        """
    registry = dbHandler.db_select(script_sql=script_sql)

    data_frame = pd.DataFrame(registry, columns=[
        'name', 'institution_id', 'count_gp', 'count_gpr'])

    return (data_frame)


def QueryByName(institution_name):
    sql = f"""
    SELECT 
        institution_id
    FROM 
        institution as i
    WHERE 
        similarity(unaccent(LOWER('{institution_name.replace("'", "''")}')), unaccent(LOWER(i.name))) > 0.8
    LIMIT 1;
    """

    result = dbHandler.db_select(sql)
    if result:
        return result[0][0]
    else:
        return None
