from adm_simcc.dao import Connection
import pandas as pd

adm_database = Connection()
mig_database = Connection(database='cimatec_v7')

def get_researchers():
    sql_script = """
        SELECT
            name,
            lattes_id
        FROM
            researcher;
        """
    registry = mig_database.select(sql_script)
    data_frame = pd.DataFrame(registry, columns=["name", "lattes_id"])
    return data_frame


def build_script_sql_researcher(data_frame):

    insert_data = str()
    for Index, Data in data_frame.iterrows():

        name = Data["name"].replace("'", "''")
        lattes_id = Data["lattes_id"]
        code = 'a43e881a-f174-4bea-b1c6-072c304dd0ab'
        insert_data += f"('{name}', '{lattes_id}', '{code}'),"

    return f"""
        INSERT INTO researcher(
        name, lattes_id, institution_id)
        VALUES {insert_data[:-1]}
        """[
        :-1
    ]


def get_actual_graduate_program(migrate_db=str()):

    sql_script = """
        SELECT
            code,
            name,
            area,
            modality,
            type,
            rating,
            institution_id,
            state,
            city,
            instituicao,
            url_image,
            region,
            sigla
        FROM
            graduate_program;
    """
    registry = mig_database.select(sql_script)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "code",
            "name",
            "area",
            "modality",
            "type",
            "rating",
            "institution_id",
            "state",
            "city",
            "instituicao",
            "url_image",
            "region",
            "sigla"
        ],
    )
    return data_frame


def build_script_sql_graduate_program(data_frame):

    insert_data = str()
    for Index, Data in data_frame.iterrows():

        code = Data["code"]
        name = Data["name"]
        area = Data["area"]
        modality = Data["modality"]
        type = Data["type"]
        rating = Data["rating"]
        institution_id = Data["institution_id"]
        state = Data["state"]
        city = Data["city"]
        instituicao = Data["instituicao"]
        url_image = Data["url_image"]
        region = Data["region"]
        sigla = Data["sigla"]

        insert_data += f"('{code}', '{name}', '{area}', '{modality}', '{type}', '{rating}', '{
            institution_id}', '{state}', '{city}', '{instituicao}', '{url_image}', '{region}', '{sigla}'),"

    return f"""
        INSERT INTO graduate_program(
        code, name, area, modality, type, rating, institution_id, state, city, instituicao, url_image, region, sigla)
            VALUES {insert_data[:-1]}
        """[
        :-1
    ]


def get_actual_graduate_program_researcher(migrate_db=str()):
    sql_script = """
        SELECT
            gp.code,
            r.lattes_id as lattes_id,
            gpr.year,
            gpr.type_
        FROM
            graduate_program_researcher gpr
        JOIN graduate_program gp
        ON gpr.graduate_program_id = gp.graduate_program_id
        JOIN researcher r
        ON r.id = gpr.researcher_id;
        """
    registry = mig_database(sql_script)

    data_frame = pd.DataFrame(
        registry, columns=["code", "lattes_id", "year", "type_"])
    return data_frame


def build_script_sql_graduate_program_researcher(Series):

    script_sql = f"""
        INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
        SELECT graduate_program_id, r.researcher_id, '{Series['year']}', '{Series['type_']}'
        FROM graduate_program
        JOIN researcher r
        ON r.lattes_id = '{Series['lattes_id']}'
        WHERE code = '{Series['code']}';
        """
    return script_sql


if __name__ == "__main__":

    if int(input('Importar os pesquisadores?\n[1-Sim / 0-Não]: ')):
        data_frame = get_researchers()

        script_sql = build_script_sql_researcher(data_frame)

        adm_database.exec(script_sql)

    if int(input('Importar os programas de pós-graduação?\n[1-Sim / 0-Não]: ')):
        data_frame_graduate_program = get_actual_graduate_program()

        script_sql = build_script_sql_graduate_program(
            data_frame_graduate_program)

        adm_database.exec(script_sql)

    if int(input('Importar os pesquisadores da pós-graduação?\n[1-Sim / 0-Não]: ')):
        data_frame_graduate_program_researcher = get_actual_graduate_program_researcher()

        for Index, Data in data_frame_graduate_program_researcher.iterrows():

            script_sql = build_script_sql_graduate_program_researcher(Data)

            adm_database.exect(script_sql)
