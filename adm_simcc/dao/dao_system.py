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


def assign_researcher(researcher):
    script_sql = """
        INSERT INTO researcher_roles (role_id, researcher_id)
        VALUES (%s, %s);
        """
    adm_database.exec(script_sql, [
        researcher[0]['role_id'],
        researcher[0]['researcher_id']
    ])


def view_researcher_roles():
    script_sql = """
        SELECT
            rr.researcher_id,
            jsonb_agg(jsonb_build_object(
                'role_id', r.id,
                'role', r.role
            )) AS roles
        FROM
            researcher_roles rr
            LEFT JOIN roles r ON r.id = rr.role_id
        GROUP BY
            rr.researcher_id;
        """
    reg = adm_database.select(script_sql)
    data_frame = pd.DataFrame(reg, columns=['researcher_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_researcher(researcher):
    script_sql = """
        DELETE FROM researcher_roles
        WHERE role_id = %s AND researcher_id = %s;
        """
    adm_database.exec(script_sql, [
        researcher[0]['role_id'],
        researcher[0]['researcher_id']
    ])


def assign_technician(technician):
    script_sql = """
        INSERT INTO technician_roles (role_id, technician_id)
        VALUES (%s, %s);
        """
    adm_database.exec(script_sql, [
        technician[0]['role_id'],
        technician[0]['technician_id']
    ])


def view_technician_roles():
    script_sql = """
        SELECT
            tr.technician_id,
            jsonb_agg(jsonb_build_object(
                'role_id', r.id,
                'role', r.role
            )) AS roles
        FROM
            technician_roles tr
            LEFT JOIN roles r ON r.id = tr.role_id
        GROUP BY
            tr.technician_id;
        """
    reg = adm_database.select(script_sql)
    data_frame = pd.DataFrame(reg, columns=['technician_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_technician(technician):
    script_sql = """
        DELETE FROM technician_roles
        WHERE role_id = %s AND technician_id = %s;
        """
    adm_database.exec(script_sql, [
        technician[0]['role_id'],
        technician[0]['technician_id']
    ])
