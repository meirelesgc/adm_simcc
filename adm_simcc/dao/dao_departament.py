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

    data_frame["img_data"] = data_frame["img_data"].apply(base64.b64decode)
    data_frame["img_data"] = data_frame["img_data"].decode("utf-8")

    return data_frame.to_dict(orient="records")
