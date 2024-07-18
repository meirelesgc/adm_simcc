import pandas as pd
from ..dao import Connection
import psycopg2

adm_database = Connection()


def departament_insert(departaments, file):
    parameters = list()

    for departament in departaments:
        # fmt: off
        parameters.append((
            departament["dep_id"], departament["org_cod"], departament["dep_nom"], 
            departament["dep_des"], departament["dep_email"], departament["dep_site"],
            departament["dep_sigla"], departament["dep_tel"], 
            # -- update values
            departament["org_cod"], departament["dep_nom"], departament["dep_des"],
            departament["dep_email"], departament["dep_site"], departament["dep_sigla"], 
            departament["dep_tel"]
        ))
        # fmt: on

    script_sql = """
        INSERT INTO ufmg_departamento
            (dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, 
            dep_tel) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            org_cod = %s, 
            dep_nom = %s,
            dep_des = %s, 
            dep_email = %s, 
            dep_site = %s, 
            dep_sigla = %s, 
            dep_tel = %s, 
            """

    adm_database.execmany(script_sql, parameters)


def departament_basic_query():
    script_sql = """
        SELECT 
            dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, 
            dep_tel
        FROM 
            ufmg_departamento;
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
        ],
    )

    return data_frame.to_dict(orient="records")
