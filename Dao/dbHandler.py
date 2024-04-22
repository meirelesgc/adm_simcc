import psycopg2
import psycopg2.extras

import env


# Função para conectar ao banco
def db_connect(database: str = None):

    if not database:
        database = env.DATABASE

    connection = psycopg2.connect(
        host=env.HOST, database=database, user=env.USER, password=env.PASSWORD
    )
    cursor = connection.cursor()
    return connection, cursor


# Função para inserir dados
def db_script(script_sql: str, database: str = None):
    connection, cursor = db_connect(database)

    try:
        cursor.execute(script_sql)
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 0

    cursor.close()
    connection.close()


# Função para consultas
def db_select(script_sql: str, database: str = None, rows: int = 0):
    connection, cursor = db_connect(database)

    try:
        cursor.execute(script_sql)

        if rows == 0:
            recset = cursor.fetchall()
        elif rows == -1:
            recset = cursor.fetchone()
        else:
            recset = cursor.fetchmany(rows)

        registros = []
        for rec in recset:
            registros.append(rec)

        cursor.close()
        connection.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        return 0

    return registros
