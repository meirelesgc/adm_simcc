import pandas as pd
from ..dao import Connection
from ..models.technician import ListTechnician

adm_database = Connection()


def technician_insert(ListTechnician: ListTechnician):
    script_sql = """
        DELETE FROM ufmg_technician
        WHERE semester = %s;
        """
    year = ListTechnician.list_technician[0].year_charge
    semester = ListTechnician.list_technician[0].semester
    adm_database.exec(script_sql, [f"{year}.{semester}"])
    parameters = list()

    for technician in ListTechnician.list_technician:
        # fmt: off
        parameters.append((
            technician.matric, technician.ins_ufmg, technician.nome, 
            technician.genero, technician.deno_sit, technician.rt,
            technician.classe, technician.cargo, technician.nivel, 
            technician.ref, technician.titulacao, technician.setor,
            technician.detalhe_setor, technician.dting_org, technician.data_prog,
            f"{year}.{semester}"
        ))
        # fmt: on
    script_sql = """
    INSERT INTO ufmg_technician
    (matric, ins_ufmg, nome, genero, deno_sit, rt, classe, cargo, nivel, ref, 
    titulacao, setor, detalhe_setor, dting_org, data_prog, semester)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    adm_database.execmany(script_sql, parameters)


def technician_basic_query(year, semester):

    parameters = list()
    if year or semester:
        parameters.append(f"{year}.{semester}")
        filter_semester = """
            WHERE semester = %s
            """
    else:
        filter_semester = """
            WHERE semester = (SELECT MAX(semester) FROM ufmg_technician)
            """

    script_sql = f"""
        SELECT 
            matric, ins_ufmg, nome, genero, deno_sit, rt, classe, cargo, nivel, ref, 
            titulacao, setor, detalhe_setor, dting_org, data_prog, semester
        FROM
            ufmg_technician
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
