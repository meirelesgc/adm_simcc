from ..dao import Connection
import pandas as pd

adm_database = Connection()


def create_new_role(role):
    script_sql = """
        INSERT INTO UFMG.roles (role)
        VALUES (%s)
        """
    adm_database.exec(script_sql, [role])


def view_roles():
    script_sql = """
        SELECT id, role
        FROM roles
        """
    reg = adm_database.select(script_sql)

    data_frame = pd.DataFrame(reg, columns=['id', 'role'])

    return data_frame.to_dict(orient='records')


def update_role(role):
    script_sql = """
        UPDATE roles
        SET role = %s
        WHERE id = %s;
        """
    adm_database.exec(script_sql, [role[0]['role'], role[0]['id']])


def delete_roles(role):
    script_sql = """
        DELETE FROM roles
        WHERE id = %s;
        """
    adm_database.exec(script_sql, [role['id']])

