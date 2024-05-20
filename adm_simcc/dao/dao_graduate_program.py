import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.graduate_program import ListGraduateProgram, GraduateProgram


adm_database = Connection()


def graduate_program_insert(ListGraduateProgram: ListGraduateProgram):
    values = str()
    for graduate_program in ListGraduateProgram.graduate_program_list:
        values += f"""(
            '{graduate_program.graduate_program_id}',
            '{graduate_program.code}',
            '{graduate_program.name}',
            '{graduate_program.area}',
            '{graduate_program.modality}',
            '{graduate_program.type}',
            '{graduate_program.rating}',
            '{graduate_program.institution_id}',
            '{graduate_program.city}',
            '{graduate_program.url_image}',
            '{graduate_program.description}',
            '{graduate_program.visible}'),"""

    # Criação do script de insert.
    # Unifiquei em um unico comando para facilitar
    # o retorno da mensagem de erro
    script_sql = f"""
        INSERT INTO public.graduate_program(
            graduate_program_id,
            code,
            name,
            area,
            modality,
            type,
            rating,
            institution_id,
            city,
            url_image,
            description,
            visible)
            VALUES {values[:-1]};
        """
    adm_database.exec(script_sql)


def graduate_program_update(graduate_program_id: UUID4):
    script_sql = f"""
        UPDATE graduate_program
        SET visible = NOT visible
        WHERE graduate_program_id = '{graduate_program_id}';
        """
    adm_database.exec(script_sql)


def graduate_program_basic_query(institution_id: UUID4):
    script_sql = f"""
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
            COUNT(CASE WHEN gr.type_ = 'COLABORADOR' THEN 1 END) as qtd_colaborador
        FROM
            graduate_program gp
        LEFT JOIN
            graduate_program_researcher gr ON gp.graduate_program_id = gr.graduate_program_id
        WHERE
            gp.institution_id = '{institution_id}'
        GROUP BY
            gp.graduate_program_id, gp
        """

    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
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
            "qtd_colaborador",
        ],
    )

    script_sql = f"""
        SELECT 
            graduate_program_id,
            COUNT(researcher_id) as qtr_discente
        FROM 
            graduate_program_student 
        GROUP BY 
            graduate_program_id
        """
    registry = adm_database.select(script_sql)

    data_frame = pd.merge(
        data_frame,
        pd.DataFrame(registry, columns=["graduate_program_id", "qtr_discente"]),
        how="left",
        on="graduate_program_id",
    )
    return data_frame.to_dict(orient="records")


def graduate_program_delete(graudate_program_id: UUID4):
    script_sql = f"""
        DELETE FROM graduate_program_researcher
        WHERE graduate_program_id = '{graudate_program_id}';

        DELETE FROM graduate_program
        WHERE graduate_program_id = '{graudate_program_id}';
        """

    adm_database.exec(script_sql)


def graduate_program_fix(Graduate_program: GraduateProgram):
    script_sql = f"""
        UPDATE graduate_program
        SET
            code = '{Graduate_program.code}',
            name = '{Graduate_program.name}',
            area = '{Graduate_program.area}',
            modality = '{Graduate_program.modality}',
            type = '{Graduate_program.type}',
            rating = '{Graduate_program.rating}',
            institution_id = '{Graduate_program.institution_id}',
            state = '{Graduate_program.state}',
            city = '{Graduate_program.city}',
            region = '{Graduate_program.region}',
            instituicao = '{Graduate_program.instituicao}',
            url_image = '{Graduate_program.url_image}',
            sigla = '{Graduate_program.sigla}',
            description = '{Graduate_program.description}',
            visible = '{Graduate_program.visible}'
        WHERE
            graduate_program_id = '{Graduate_program.graduate_program_id}';
        """
    adm_database.exec(script_sql)


def graduate_program_count(institution_id: UUID4 = None):
    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE institution_id = '{institution_id}'"

    script_sql = f"SELECT COUNT(*) FROM graduate_program {filter_institution}"

    registry = adm_database.select(script_sql)

    # psycopg2 retorna uma lista de truplas,
    # quero apenas o primeiro valor da primeira lista
    return registry[0][0]
