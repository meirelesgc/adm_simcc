from ..dao import Connection
from ..models import UserModel
import pandas as pd

adm_database = Connection()


def create_user(User: UserModel):
    SCRIPT_SQL = """
        INSERT INTO users (display_name, email, uid, photo_url, shib_uid)
        VALUES (%s, %s, %s, %s);
        """
    adm_database.exec(SCRIPT_SQL,
                      (User.displayName, User.email, User.uid, User.photoURL))


def select_user(uid):
    SCRIPT_SQL = """
        SELECT u.user_id, 
            display_name, 
            email, 
            uid, 
            photo_url, 
            shib_uid,
            jsonb_agg(jsonb_build_object('id', p.id, 'role_id', p.role_id, 'permission', p.permission)) AS permission
        FROM users u
        LEFT JOIN users_roles ur ON ur.user_id = u.user_id
        LEFT JOIN roles r ON r.id = ur.role_id
        LEFT JOIN permission p ON p.role_id = ur.role_id
        WHERE uid = %s OR shib_uid = %s
        GROUP BY u.user_id, display_name, email, uid, photo_url, shib_uid;
        """
    print(SCRIPT_SQL)
    registry = adm_database.select(SCRIPT_SQL, [uid, uid])

    data_frame = pd.DataFrame(registry,
                              columns=[
                                  'user_id', 'display_name', 'email', 'uid',
                                  'photo_url', 'shib_uid', 'permissions'
                              ])

    return data_frame.to_dict(orient='records')


def list_users():
    SCRIPT_SQL = """
        SELECT user_id, displayName, email, uid, photoURL
        FROM users;
        """
    registry = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(
        registry,
        columns=['user_id', 'displayName', 'email', 'uid', 'photoURL'])

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


def assign_user(user):
    SCRIPT_SQL = """
        INSERT INTO users_roles (role_id, user_id)
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
            users_roles ur
            LEFT JOIN roles r ON r.id = ur.role_id
            LEFT JOIN
        GROUP BY
            ur.user;
        """
    reg = adm_database.select(SCRIPT_SQL)
    data_frame = pd.DataFrame(reg, columns=['user_id', 'roles'])
    return data_frame.to_dict(orient='records')


def unassign_user(user):
    SCRIPT_SQL = """
        DELETE FROM users_roles
        WHERE role_id = %s AND user_id = %s;
        """
    adm_database.exec(
        SCRIPT_SQL, [user[0]['role_id'], user[0]['user_id']])
