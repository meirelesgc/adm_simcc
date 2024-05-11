import pandas as pd
from pydantic import UUID4

from ..dao import Connection
from ..models.graduate_program import GraduateProgram

adm_database = Connection()


def graduate_program_insert(Graduate_program: GraduateProgram):
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
            state, 
            city, 
            region, 
            instituicao, 
            url_image, 
            sigla, 
            description, 
            visible)
	    VALUES (    
            '{Graduate_program.graduate_program_id}', 
            '{Graduate_program.code}', 
            '{Graduate_program.name}', 
            '{Graduate_program.area}', 
            '{Graduate_program.modality}', 
            '{Graduate_program.type}', 
            '{Graduate_program.rating}', 
            '{Graduate_program.institution_id}', 
            '{Graduate_program.state}', 
            '{Graduate_program.city}', 
            '{Graduate_program.region}', 
            '{Graduate_program.instituicao}', 
            '{Graduate_program.url_image}', 
            '{Graduate_program.sigla}', 
            '{Graduate_program.description}', 
            '{Graduate_program.visible}');
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
            graduate_program_id, 
            code, 
            name, 
            area, 
            modality, 
            type, 
            rating, 
            institution_id,
            description, 
            url_image,
            city, 
            visible, 
            created_at, 
            updated_at 
        FROM 
            graduate_program 
        WHERE 
            institution_id = '{institution_id}';
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
        ],
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
