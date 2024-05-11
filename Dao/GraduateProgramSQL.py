# Para conseguir importar os modulos de projeto em tempo de execução desse script
import sys

import pandas as pd

import Dao.dbHandler as dbHandler
from Model.GraduateProgram import GraduateProgram

sys.path.append("../")


def Insert(GraduateProgram):
    sql = """
    INSERT INTO graduate_program (graduate_program_id, code, name, area, modality, TYPE, rating, institution_id, description, url_image, city, visible)
    VALUES
        ('{graduate_program_id}', '{code}', '{name}', '{area}', '{modality}', '{TYPE}', '{rating}', '{institution_id}', '{description}', '{url_image}', '{city}', '{visible}')
    """.format(
        graduate_program_id=GraduateProgram.graduate_program_id,
        code=GraduateProgram.code,
        name=GraduateProgram.name,
        area=GraduateProgram.area,
        modality=GraduateProgram.modality,
        TYPE=GraduateProgram.type,
        rating=GraduateProgram.rating,
        institution_id=GraduateProgram.institution_id,
        description=GraduateProgram.description,
        url_image=GraduateProgram.url_image,
        city=GraduateProgram.city,
        visible=GraduateProgram.visible,
    )

    return dbHandler.db_script(sql)


def Query(institution_id):
    sql = f"""
        SELECT 
            gp.graduate_program_id, 
            gp.code, 
            gp.name, 
            gp.area, 
            gp.modality, 
            gp.type, 
            gp.rating, 
            gp.institution_id,
            gp.description, 
            gp.url_image,
            gp.city, 
            gp.visible, 
            gp.created_at, 
            gp.updated_at,
            COUNT(CASE WHEN gr.type_ = 'PERMANENTE' THEN 1 END) as qtd_permanente,
            COUNT(CASE WHEN gr.type_ = 'DISCENTE' THEN 1 END) as qtd_discente,
            COUNT(CASE WHEN gr.type_ = 'COLABORADOR' THEN 1 END) as qtd_colaborador
        FROM 
            graduate_program gp
        LEFT JOIN
            graduate_program_researcher gr ON gp.graduate_program_id = gr.graduate_program_id
        WHERE 
            gp.institution_id = '{institution_id}'
        GROUP BY
            gp.graduate_program_id
        """
    
    data_frame = pd.DataFrame(
        dbHandler.db_select(sql),
        columns=[
            "graduate_program_id",
            "code",
            "name",
            "area",
            "modality",
            "type",
            "rating",
            "institution_id",
            "description",
            "url_image",
            "city",
            "visible",
            "created_at",
            "updated_at",
            "qtd_permanente",
            "qtd_discente",
            "qtd_colaborador"
        ],
    )
    return data_frame.to_dict(orient='records')


def Update(ID):
    sql = """UPDATE graduate_program SET visible = NOT visible WHERE graduate_program_id = '{filter}';""".format(
        filter=ID
    )
    dbHandler.db_script(script_sql=sql)
    return "Update concluido"


def Delete(ID):
    sql = """DELETE FROM graduate_program WHERE graduate_program_id = '{filter}';""".format(
        filter=ID
    )
    dbHandler.db_script(script_sql=sql)
    return "Delete concluido"


def Fix(GraduateProgram):
    sql = """UPDATE graduate_program
	SET graduate_program_id='{graduate_program_id}', code='{code}', name='{name}', area='{area}', modality='{modality}', type='{TYPE}', rating='{rating}', institution_id='{institution_id}', description='{description}', url_image='{url_image}', city='{city}', visible='{visible}'
	WHERE graduate_program_id = '{filter}';""".format(
        graduate_program_id=GraduateProgram.graduate_program_id,
        code=GraduateProgram.code,
        name=GraduateProgram.name,
        area=GraduateProgram.area,
        modality=GraduateProgram.modality,
        TYPE=GraduateProgram.type,
        rating=GraduateProgram.rating,
        institution_id=GraduateProgram.institution_id,
        description=GraduateProgram.description,
        url_image=GraduateProgram.url_image,
        city=GraduateProgram.city,
        visible=GraduateProgram.visible,
        filter=GraduateProgram.graduate_program_id,
    )
    dbHandler.db_script(script_sql=sql)
    return "Update concluido"


def query_count():
    script_sql = "SELECT COUNT(*) FROM graduate_program;"

    return dbHandler.db_select(script_sql=script_sql, rows=-1)[0]
