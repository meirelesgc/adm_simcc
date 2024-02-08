import sys
from os.path import dirname, abspath

PATH = dirname(dirname(abspath(__file__)))
sys.path.append(PATH)

from Dao import dbHandler
import pandas as pd


def get_actual_researchers():
    sql_script = """
        SELECT 
            r.name, 
            r.lattes_id,
            CASE
                WHEN i.name = 'Instituto Federal da Bahia' THEN 6
                WHEN i.name = 'Universidade Federal da Bahia ' THEN 1
                WHEN i.name = 'Universidade do Estado da Bahia' THEN 2
                WHEN i.name = 'Universidade Estadual de Santa Cruz' THEN 3
                ELSE 0
            END as adm_code
        FROM
            researcher as r
        JOIN
            institution as i
        ON
            i.id = r.institution_id;
        """
    registry = dbHandler.db_select(sql_script)

    data_frame = pd.DataFrame(registry, columns=["name", "lattes_id", "adm_code"])
    return data_frame


def build_script_sql(data_frame):

    INSTITUICAO_INVALIDA = 0
    insert_data = str()
    for Index, Data in data_frame.iterrows():

        name = Data["name"].replace("'", "''")
        lattes_id = Data["lattes_id"]
        code = Data["adm_code"]
        if code != INSTITUICAO_INVALIDA:
            insert_data += f"('{name}', '{lattes_id}', {code}),"

    return f"""
        INSERT INTO researcher(
	    name, lattes_id, institution_id)
	    VALUES {insert_data[:-1]}
        """[
        :-1
    ]


if __name__ == "__main__":
    data_frame = get_actual_researchers()

    script_sql = build_script_sql(data_frame)

    dbHandler.db_script(script_sql, database="adm_simcc")
