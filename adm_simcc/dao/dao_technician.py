import pandas as pd
from ..dao import Connection
from ..models.technician import ListTechnician, ListRole    

adm_database = Connection()


def technician_insert(ListTechnician: ListTechnician):
    script_sql = """
        DELETE FROM UFMG.technician
        WHERE semester = %s;
        """
    year = ListTechnician.list_technician[0].year_charge
    semester = ListTechnician.list_technician[0].semester
    adm_database.exec(script_sql, [f"{year}.{semester}"])
    parameters = list()

    for technician in ListTechnician.list_technician:
        # fmt: off
        parameters.append((
            technician.matric, technician.insUFMG, technician.nome, 
            technician.genero, technician.denoSit, technician.rt,
            technician.classe, technician.cargo, technician.nivel, 
            technician.ref, technician.titulacao, technician.setor,
            technician.detalheSetor, technician.dtIngOrg, technician.dataProg,
            f"{year}.{semester}"
        ))
        # fmt: on
    script_sql = """
    INSERT INTO UFMG.technician
    (matric, ins_ufmg, nome, genero, deno_sit, rt, classe, cargo, nivel, ref, 
    titulacao, setor, detalhe_setor, dting_org, data_prog, semester)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    adm_database.execmany(script_sql, parameters)


def technician_basic_query(year, semester, departament):

    parameters = list()

    if year or semester:
        parameters.append(f"{year}.{semester}")
        filter_semester = """
            AND semester = %s
            """
    else:
        filter_semester = """
            AND semester = (SELECT MAX(semester) FROM UFMG.technician)
            """

    script_sql = f"""
        SELECT
            technician_id, matric, ins_ufmg, nome, genero, deno_sit, rt, classe,
            cargo, nivel, ref, titulacao, setor, detalhe_setor, dting_org,
            data_prog, semester
        FROM
            UFMG.technician
        WHERE
        1 = 1
        {filter_semester}
        """

    registry = adm_database.select(script_sql, parameters)

    data_frame = pd.DataFrame(
        registry,
        columns=[
            "technician_id",
            "matric",
            "ins_ufmg",
            "nome",
            "genero",
            "deno_sit",
            "rt",
            "classe",
            "cargo",
            "nivel",
            "ref",
            "titulacao",
            "setor",
            "detalhe_setor",
            "dting_org",
            "data_prog",
            "semester",
        ],
    )
    return data_frame.to_dict(orient="records")


def technician_query_semester():
    script_sql = """
    SELECT
        SUBSTRING(semester, 1, 4) AS year,
        SUBSTRING(semester, 6, 1) AS semester
    FROM
        ufmg.technician
    GROUP BY semester;
    """
    registry = adm_database.select(script_sql)

    data_frame = pd.DataFrame(registry, columns=["year", "semester"])

    return data_frame.to_dict(orient="records")


def technician_insert_role(ListRole: ListRole):
    parameters = list()
    for role in ListRole.list_roles:
        parameters.append((
            role.role, role.researcher_id
        ))

    script_sql = """
        INSERT INTO technician_role (role, technician_id)
        VALUES (%s, %s)
        """

    adm_database.exec(script_sql, parameters)


def technician_query_role():
    script_sql = '''
        SELECT
            role,
            technician_id
        FROM
            technician_role
        '''

    registry = adm_database.select(script_sql)

    data_frame = pd.Dataframe(registry, columns=['role', 'technician_id'])

    return data_frame.to_dict(orient='records')
