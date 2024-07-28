import pandas as pd
from ..dao import Connection
from ..models.technician import ListTechnician

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
    filter_departament = str()

    if year or semester:
        parameters.append(f"{year}.{semester}")
        filter_semester = """
            WHERE semester = %s
            """
    else:
        filter_semester = """
            WHERE semester = (SELECT MAX(semester) FROM UFMG.technician)
            """

    if departament:
        filter_semester = """
            AND
            """
    script_sql = f"""
        SELECT 
            matric, ins_ufmg, nome, genero, deno_sit, rt, classe, cargo, nivel, ref, 
            titulacao, setor, detalhe_setor, dting_org, data_prog, semester
        FROM
            UFMG.technician
        {filter_semester}
        """

    registry = adm_database.select(script_sql, parameters)

    data_frame = pd.DataFrame(
        registry,
        columns=[
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
