from ..dao import Connection
from ..models import UserModel
import pandas as pd

adm_database = Connection()


def create_user(User: UserModel):
    SCRIPT_SQL = """
        INSERT INTO user (displayName, email, uid, photoURL)
        VALUES (%s, %s, %s, %s);
        """
    adm_database.exec(SCRIPT_SQL,
                      (User.displayName, User.email, User.uid, User.photoURL))


def select_user(uid):
    SCRIPT_SQL = """
        SELECT user_id, displayName, email, uid, photoURL
        FROM user WHERE uid = %s;
        """
    registry = adm_database.select(SCRIPT_SQL, uid)

    data_frame = pd.DataFrame(
        registry, columns=['user_id', 'displayName', 'email', 'uid', 'photoURL'])

    return data_frame.to_dict(orient='records')


def create_new_role(role):
    SCRIPT_SQL = """
        INSERT INTO roles (role)
        VALUES (%s)
        """
    adm_database.exec(SCRIPT_SQL, [role[0]['role']])


def view_roles():
    SCRIPT_SQL = """
        SELECT id, role
        FROM roles
        """
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['id', 'role'])
    return data_frame.to_dict(orient='records')


def update_role(role):
    SCRIPT_SQL = """
        UPDATE roles
        SET role = %s
        WHERE id = %s;
        """
    adm_database.exec(SCRIPT_SQL, [role[0]['role'], role[0]['id']])


def delete_role(role):
    SCRIPT_SQL = """
        DELETE FROM roles
        WHERE id = %s;
        """
    adm_database.exec(SCRIPT_SQL, [role[0]['id']])


def permission_insert(permission):
    SCRIPT_SQL = """
        INSERT INTO permission (role_id, permission)
        VALUES (%s, %s);
        """
    adm_database.exec(SCRIPT_SQL,
                      [permission[0]['role_id'], permission[0]['permission']])


def permissions_view():
    SCRIPT_SQL = """
    SELECT id, role_id, permission
    FROM permission
    """
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['id', 'role_id', 'permission'])
    return data_frame.to_dict(orient='records')


def permission_update(permission):
    SCRIPT_SQL = """
        UPDATE permission
        SET permission = %s
        WHERE id = %s;
        """
    adm_database.exec(
        SCRIPT_SQL,
        [permission[0]['permission'], permission[0]['permission_id']])


def permission_delete(permission):
    SCRIPT_SQL = """
        DELETE FROM permission
        WHERE id = %s;
        """
    adm_database.exec(SCRIPT_SQL, [permission[0]['permission_id']])


def assign_researcher(researcher):
    SCRIPT_SQL = """
        INSERT INTO researcher_roles (role_id, researcher_id)
        VALUES (%s, %s);
        """
    adm_database.exec(
        SCRIPT_SQL, [researcher[0]['role_id'], researcher[0]['researcher_id']])


def view_researcher_roles():
    SCRIPT_SQL = """
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
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['researcher_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_researcher(researcher):
    SCRIPT_SQL = """
        DELETE FROM researcher_roles
        WHERE role_id = %s AND researcher_id = %s;
        """
    adm_database.exec(
        SCRIPT_SQL, [researcher[0]['role_id'], researcher[0]['researcher_id']])


def assign_technician(technician):
    SCRIPT_SQL = """
        INSERT INTO technician_roles (role_id, technician_id)
        VALUES (%s, %s);
        """
    adm_database.exec(
        SCRIPT_SQL, [technician[0]['role_id'], technician[0]['technician_id']])


def view_technician_roles():
    SCRIPT_SQL = """
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
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['technician_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_technician(technician):
    SCRIPT_SQL = """
        DELETE FROM technician_roles
        WHERE role_id = %s AND technician_id = %s;
        """
    adm_database.exec(
        SCRIPT_SQL, [technician[0]['role_id'], technician[0]['technician_id']])


def assign_user(user):
    SCRIPT_SQL = """
        INSERT INTO user_roles (role_id, user_id)
        VALUES (%s, %s);
        """
    adm_database.exec(SCRIPT_SQL, [user[0]['role_id'], user[0]['user_id']])


def view_user_roles():
    SCRIPT_SQL = """
        SELECT
            ur.user_id,
            jsonb_agg(jsonb_build_object(
                'role_id', r.id,
                'role', r.role
            )) AS roles
        FROM
            user_roles ur
            LEFT JOIN roles r ON r.id = ur.role_id
        GROUP BY
            ur.user;
        """
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['user_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_user(user):
    SCRIPT_SQL = """
        DELETE FROM user_roles
        WHERE role_id = %s AND user_id = %s;
        """
    adm_database.exec(
        SCRIPT_SQL, [user[0]['role_id'], user[0]['user_id']])
