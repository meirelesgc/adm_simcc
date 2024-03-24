import os
import pandas as pd
from Dao import dbHandler as bd
from pprint import pprint


def get_institution_data():
    script_sql = "SELECT institution_id, name, acronym, lattes_id FROM institution;"

    registry = bd.db_select(script_sql=script_sql)

    data_frame = pd.DataFrame(
        registry,
        columns=["institution_id", "name", "acronym", "lattes_id"],
    )

    for Index, Data in data_frame.iterrows():
        print(f"[{Index}] - {Data['name']} - {Data['acronym']}")
    institution_index = int(
        input(f"Anexar os programas de graduação na instituição [Index - 0/{Index}]: ")
    )
    return data_frame.iloc[institution_index]


def get_data_frame(file_name: str):
    if file_name.endswith(".csv"):
        try:
            return pd.read_csv(f"Files/{file_name}", encoding="utf-8", delimiter=";")
        except:
            return pd.read_csv(f"Files/{file_name}", encoding="utf-8", delimiter=",")
    elif file_name.endswith("xls"):
        return pd.read_excel(f"Files/{file_name}", engine="xlrd")
    elif file_name.endswith("xlsx"):
        return pd.read_excel(f"Files/{file_name}", engine="openpyxl")


def select_type_graduate_program(serie_gp: pd.Series) -> str:
    max_rating = max(serie_gp["ME"], serie_gp["DO"], serie_gp["MP"], serie_gp["DP"])

    type = list()
    if (serie_gp["ME"] != "-") or (serie_gp["MP"] != "-"):
        type.append("MESTRADO")
    if (serie_gp["DO"] != "-") or (serie_gp["DP"] != "-"):
        type.append("DOUTORADO")

    return str("/").join(type), max_rating


def sanitize_string(string: str) -> str:
    sanitized_string = string.strip().replace("'", "")
    return sanitized_string


if __name__ == "__main__":
    if int(input("Cadastrar programas de graduação?\n[1-Sim / 0-Não]: ")):

        data_frame_institutions = get_institution_data()
        localização = str(input("Digite a cidade do programa: "))

        file_list = os.listdir("Files")
        for Index in range(len(file_list)):
            print(f"[{Index}] - {file_list[Index]}")
        file_index = int(
            input(
                f"Anexar os programas de graduação na instituição [Index - 0/{Index}]: "
            )
        )

        for Index, Data in get_data_frame(file_list[file_index]).iterrows():
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

    if int(input("Importar pesquisadores?\n[1-Sim / 0-Não]: ")):

        data_frame_institutions = get_institution_data()

        file_list = os.listdir("Files")
        for Index in range(len(file_list)):
            print(f"[{Index}] - {file_list[Index]}")
        file_index = int(
            input(
                f"Anexar os programas de graduação na instituição [Index - 0/{Index}]: "
            )
        )

        for Index, Data in get_data_frame(file_list[file_index]).dropna().iterrows():
            if not bd.db_select(
                f"SELECT 'True' FROM researcher WHERE lattes_id = '{Data['Lattes'][-16:]}'"
            ):
                script_sql = f"""
                    INSERT INTO researcher(
                    name, lattes_id, institution_id)
                    VALUES ('{Data['Name'].title()}', '{Data['Lattes'][-16:]}', '{data_frame_institutions['institution_id']}');
                    """
                bd.db_script(script_sql=script_sql)

            type_ = str(Data["type_"]).upper()

            script_sql = f"""
            INSERT INTO graduate_program_researcher (graduate_program_id, researcher_id, year, type_)
            SELECT gp.graduate_program_id, r.researcher_id, {2024}, '{type_}'
            FROM researcher r
            JOIN graduate_program gp
            ON gp.code ILIKE '{Data['code']}'
            WHERE r.lattes_id = '{Data['Lattes'][-16:]}';"""

            bd.db_script(script_sql=script_sql)
