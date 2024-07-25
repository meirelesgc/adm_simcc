import pandas as pd
from ..dao import Connection
import psycopg2

adm_database = Connection()


def departament_insert(departaments, file):
    parameters = list()

    for i, departament in enumerate(departaments):
        # fmt: off
        parameters.append((
            departament["dep_id"], departament["org_cod"], departament["dep_nom"], 
            departament["dep_des"], departament["dep_email"], departament["dep_site"],
            departament["dep_sigla"], departament["dep_tel"], psycopg2.Binary(file[f'img_data_{i}'].read()) if f'img_data_{i}' in file else None,
            # -- update values
            departament["org_cod"], departament["dep_nom"], departament["dep_des"],
            departament["dep_email"], departament["dep_site"], departament["dep_sigla"], 
            departament["dep_tel"], psycopg2.Binary(file[f'img_data_{i}'].read()) if f'img_data_{i}' in file else None,
        ))
        # fmt: on

    script_sql = """
        INSERT INTO ufmg_departament
            (dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, 
            dep_tel, img_data) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            org_cod = %s, 
            dep_nom = %s,
            dep_des = %s, 
            dep_email = %s, 
            dep_site = %s, 
            dep_sigla = %s, 
            dep_tel = %s, 
            img_data = %s
            """

    adm_database.execmany(script_sql, parameters)


def departament_basic_query():
    script_sql = """
        SELECT 
            dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, 
            dep_tel, img_data
        FROM 
            ufmg_departament;
        """
    reg = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        reg,
        columns=[
            "dep_id",
            "org_cod",
            "dep_nom",
            "dep_des",
            "dep_email",
            "dep_site",
            "dep_sigla",
            "dep_tel",
            "img_data",
        ],
    )

    return data_frame.to_dict(orient="records")
