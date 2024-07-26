import pandas as pd
from ..dao import Connection
import psycopg2
import base64

adm_database = Connection()


def departament_insert(departaments, file):
    parameters = list()

    # fmt: off
    parameters =[
        departaments["dep_id"], departaments["org_cod"],
        departaments["dep_nom"], departaments["dep_des"],
        departaments["dep_email"], departaments["dep_site"],
        departaments["dep_sigla"], departaments["dep_tel"],
        psycopg2.Binary(file["img_data"].read())
    ]
    # fmt: on
    script_sql = """
        INSERT INTO UFMG.departament
            (dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla,
             dep_tel, img_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    adm_database.exec(script_sql, parameters)


def departament_basic_query():
    script_sql = """
        SELECT 
            dep_id, org_cod, dep_nom, dep_des, dep_email, dep_site, dep_sigla, 
            dep_tel, img_data
        FROM 
            UFMG.departament;
        """
    reg = adm_database.select(script_sql)

    columns = [
        "dep_id",
        "org_cod",
        "dep_nom",
        "dep_des",
        "dep_email",
        "dep_site",
        "dep_sigla",
        "dep_tel",
        "img_data",
    ]
    result = list()
    for row in reg:
        row_dict = dict(zip(columns, row))
        row_dict["img_data"] = (
            base64.b64encode(row_dict["img_data"]).decode("utf-8")
            if row_dict["img_data"]
            else None
        )
        result.append(row_dict)

    return result


def departament_delete(dep_id):
    script_sql = """
        DELETE FROM UFMG.departament
        WHERE dep_id = %s;
        """
    adm_database.exec(script_sql, [dep_id])
