import pandas as pd
from Dao import dbHandler as bd
from pprint import pprint


def get_institutions():
    script_sql = "SELECT institution_id, name, acronym, lattes_id FROM institution;"

    registry = bd.db_select(script_sql=script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["institution_id", "name", "acronym", "lattes_id"],
    )

    return data_frame


def get_graduate_program():
    return pd.read_csv("Files/graduate_program.csv", encoding="utf-8", delimiter=";")


def select_type_graduate_program(serie_gp: pd.Series) -> str:
    max_rating = max(serie_gp["ME"], serie_gp["DO"], serie_gp["MP"], serie_gp["DP"])

    type = list()
    if (serie_gp["ME"] != "-") or (serie_gp["MP"] != "-"):
        type.append("MESTRADO")
    if (serie_gp["DO"] != "-") or (serie_gp["DP"] != "-"):
        type.append("DOUTORADO")

    return str("/").join(type), max_rating


if __name__ == "__main__":
    data_frame_institutions = get_institutions()
    for Index, Data in data_frame_institutions.iterrows():
        print(f"[{Index}] - {Data['name']} - {Data['acronym']}")
    institution_index = int(
        input(f"Anexar os programas de graduação na instituição [Index - 0/{Index}]: ")
    )
    data_frame_institutions = data_frame_institutions.iloc[institution_index]

    localização = str(input("Digite a cidade do programa: "))

    for Index, Data in get_graduate_program().iterrows():

        type = select_type_graduate_program(Data)

        script_sql = f"""
            INSERT INTO graduate_program(
            code, name, area, modality, type, rating, institution_id, city, instituicao, sigla)
            VALUES 
                ('{Data['Código']}', 
                '{Data['Programa']}', 
                '{Data['Área de Avaliação'].strip()}', 
                '{Data['Modalidade']}', 
                '{type[0]}', 
                '{type[1]}', 
                '{data_frame_institutions['institution_id']}', 
                '{localização}', 
                '{Data["Instituição de Ensino"]}', 
                '{data_frame_institutions["acronym"]}')
            """
        bd.db_script(script_sql=script_sql)
