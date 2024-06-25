from adm_simcc.dao import Connection
import pandas as pd

df = pd.read_csv("files/asd.csv.csv")
print(df.columns)
adm = Connection()

for i, j in df.iterrows():
    script_sql = f"""
    INSERT INTO researcher (name, lattes_id, institution_id)
    VALUES ('{j['NOME']}', '{j['ID_LATTES']}', '{j['INSTITUICAO']}')
    """
    try:
        adm.exec(script_sql)
    except:
        print(script_sql)
