from ..dao import Connection
import pandas as pd

adm_database = Connection()


def create_new_role(role):
    script_sql = """
        INSERT INTO roles (role)
        VALUES (%s)
        """
    adm_database.exec(script_sql, [role[0]['role']])


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


def delete_role(role):
    script_sql = """
        DELETE FROM roles
        WHERE id = %s;
        """
    adm_database.exec(script_sql, [role[0]['id']])


def permission_insert(permission):
    script_sql = """
        INSERT INTO permission (role_id, permission)
        VALUES (%s, %s);
        """
    adm_database.exec(
        script_sql, [permission[0]['role_id'], permission[0]['permission']])


def permissions_view():
    script_sql = """
    SELECT id, role_id, permission
    FROM permission
    """
    reg = adm_database.select(script_sql)
    data_frame = pd.DataFrame(reg, columns=['id', 'role_id', 'permission'])
    return data_frame.to_dict(orient='records')


def permission_update(permission):

    script_sql = """
        UPDATE permission
        SET permission = %s
        WHERE id = %s;
        """
    adm_database.exec(
        script_sql,
        [permission[0]['permission'], permission[0]['permission_id']])


def permission_delete(permission):
    script_sql = """
        DELETE FROM permission
        WHERE id = %s;
        """
    adm_database.exec(script_sql, [permission[0]['permission_id']])
