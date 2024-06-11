import os
import pandas as pd
from zeep import Client

from pydantic import UUID4

from ..dao import Connection
from ..models.researcher import ListResearchers, ListSubsidies

adm_database = Connection()
simcc_database = Connection(database=os.environ["SIMCC_DATABASE"])
CNPq = Client("http://servicosweb.cnpq.br/srvcurriculo/WSCurriculo?wsdl")


def researcher_insert(ListResearchers: ListResearchers):

    values = str()

    for researcher in ListResearchers.researcher_list:
        values += f"""(
            '{researcher.researcher_id}',
            '{researcher.name}',
            '{researcher.lattes_id}',
            '{researcher.institution_id}'),"""

    # Criação do script de insert.
    # Unifiquei em um unico comando para facilitar
    # o retorno da mensagem de erro
    script_sql = f"""
        INSERT INTO researcher
        (researcher_id, name, lattes_id, institution_id)
        VALUES {values[:-1]};
        """
    adm_database.exec(script_sql)


def researcher_delete(researcher_id: UUID4):
    script_sql = f"""
        DELETE FROM graduate_program_researcher
        WHERE researcher_id = '{researcher_id}';

        DELETE FROM graduate_program_student
        WHERE researcher_id = '{researcher_id}';

        DELETE FROM researcher
        WHERE researcher_id = '{researcher_id}';
        """
    adm_database.exec(script_sql)


def researcher_basic_query(
    institution_id: UUID4 = None,
    researcher_name: str = None,
    rows: int = None,
    lattes_id: str = None,
):
    filter_name = filter_limit = filter_institution = filter_lattes_id = str()
    if institution_id:
        filter_institution = f"""
            AND r.institution_id = '{institution_id}'
            """
    if researcher_name:
        researcher_name = researcher_name.replace("'", "''")
        filter_name = f"""
            AND name ILIKE '{researcher_name}%'
            """
    if rows:
        filter_limit = f"LIMIT {rows}"

    if lattes_id:
        filter_lattes_id = f"AND lattes_id = '{lattes_id}'"

    script_sql = f"""
        SELECT DISTINCT
            r.researcher_id,
            r.name,
            r.lattes_id,
            r.institution_id,
            r.created_at,
            jsonb_agg(jsonb_build_object(
                'subsidy_id', s.id,
                'modality_code', s.modality_code,
                'category_level_code', s.category_level_code
            )) AS subsidies
        FROM
            researcher r
        LEFT JOIN subsidy s ON s.researcher_id = r.researcher_id 
        WHERE
            r.researcher_id NOT IN (SELECT researcher_id FROM public.graduate_program_student)
            {filter_institution}
            {filter_name}
            {filter_lattes_id}
        GROUP BY
            r.researcher_id,
            r.name,
            r.lattes_id,
            r.institution_id,
            r.created_at
        ORDER BY
            r.created_at DESC
            {filter_limit};
        """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "researcher_id",
            "name",
            "lattes_id",
            "institution_id",
            "created_at",
            "subsidies",
        ],
    )
    script_sql = f"""
        SELECT
            r.lattes_id,
            r.last_update
        FROM
            researcher r
        """

    registry = simcc_database.select(script_sql=script_sql)
    data_frame_simcc = pd.DataFrame(registry, columns=["lattes_id", "last_update"])
    data_frame = pd.merge(data_frame, data_frame_simcc, how="left", on="lattes_id")

    return data_frame.fillna("Não esta atualizado").to_dict(orient="records")


def researcher_count(institution_id: UUID4 = None):
    filter_institution = str()
    if institution_id:
        filter_institution = f"WHERE institution_id = '{institution_id}'"

    script_sql = f"SELECT COUNT(*) FROM researcher {filter_institution}"

    registry = adm_database.select(script_sql)

    # psycopg2 retorna uma lista de truplas,
    # quero apenas o primeiro valor da primeira lista
    return registry[0][0]


def researcher_query_name(researcher_name: str):
    script_sql = f"""
    SELECT
        researcher_id
    FROM
        researcher as r
    WHERE
        similarity(unaccent(LOWER('{researcher_name.replace("'", "''")}')), unaccent(LOWER(r.name))) > 0.4
    LIMIT 1;
    """

    registry = adm_database.select(script_sql)

    if registry:
        return registry[0][0]
    else:
        return None


def researcher_search_id(lattes_id):
    script_sql = f"""
        SELECT
            researcher_id 
        FROM
            researcher
        WHERE
            lattes_id = '{lattes_id}'
        """
    researcher_id = adm_database.select(script_sql)

    if researcher_id:
        return researcher_id[0][0]
    else:
        return ...


def researcher_insert_grant(ListSubsidies: ListSubsidies):

    values = str()

    for subsidy in ListSubsidies.grant_list:
        values += f"""(
                '{researcher_search_id(subsidy.id_lattes)}', 
                '{subsidy.cod_modalidade}', 
                '{subsidy.nome_modalidade}', 
                '{subsidy.titulo_chamada}', 
                '{subsidy.cod_categoria_nivel}', 
                '{subsidy.nome_programa_fomento}', 
                '{subsidy.nome_instituto}', 
                '{subsidy.quant_auxilio}',
                '{subsidy.quant_bolsa}'),"""

    script_sql = f"""
        INSERT INTO public.subsidy(
            researcher_id, 
            modality_code, 
            modality_name, 
            call_title, 
            category_level_code, 
            funding_program_name, 
            institute_name, 
            aid_quantity, 
            scholarship_quantity)
            VALUES {values[:-1]};
        """

    adm_database.exec(script_sql)


def researcher_query_grant(institution_id):

    filter_institution = str()
    if institution_id:
        filter_institution = f"""
                AND r.institution_id = '{institution_id}'
                """

    script_sql = f"""
        SELECT 
            s.id, 
            s.researcher_id,
            r.name,
            s.modality_code, 
            s.modality_name, 
            s.call_title, 
            s.category_level_code, 
            s.funding_program_name, 
            s.institute_name, 
            s.aid_quantity, 
            s.scholarship_quantity
        FROM 
            subsidy s
            LEFT JOIN researcher r ON s.researcher_id = r.researcher_id
        WHERE
            1 = 1
            {filter_institution}
        """

    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "id",
            "researcher_id",
            "name",
            "modality_code",
            "modality_name",
            "call_title",
            "category_level_code",
            "funding_program_name",
            "institute_name",
            "aid_quantity",
            "scholarship_quantity",
        ],
    )

    return data_frame.to_dict(orient="records")
