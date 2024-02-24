from Dao import dbHandler
import pandas as pd


def get_actual_researchers():
    sql_script = """
        SELECT 
            r.name, 
            r.lattes_id,
            COALESCE(i.id, '498cadc8-b8f6-4008-902e-76281101237d') AS institution_id
        FROM
            researcher r
        LEFT JOIN
            institution i
        ON
            i.id = r.institution_id
        AND
            i.acronym IN ('UESB', 'UFBA', 'UNEB', 'UESC');
        """
    registry = dbHandler.db_select(sql_script, database="simcc_")

    data_frame = pd.DataFrame(registry, columns=["name", "lattes_id", "institution_id"])
    return data_frame


def build_script_sql(data_frame):

    insert_data = str()
    for Index, Data in data_frame.iterrows():

        name = Data["name"].replace("'", "''")
        lattes_id = Data["lattes_id"]
        code = Data["institution_id"]
        insert_data += f"('{name}', '{lattes_id}', '{code}'),"

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

    dbHandler.db_script(script_sql)
