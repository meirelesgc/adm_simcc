from ..dao import Connection
from ..models import UserModel
import pandas as pd

adm_database = Connection()


def create_user(User: UserModel):

    SCRIPT_SQL = """
    SELECT lattes_id FROM researcher WHERE
    unaccent(name) ILIKE unaccent(%s) LIMIT 1;
    """

    lattes_id = adm_database.select(SCRIPT_SQL, [User.displayName])

    if lattes_id:
        User.lattes_id = lattes_id[0][0]
    SCRIPT_SQL = """
        INSERT INTO users (display_name, email, uid, photo_url, shib_uid, linkedin, provider, lattes_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
    adm_database.exec(SCRIPT_SQL, [
        User.displayName, User.email, User.uid,
        str(User.photoURL), User.shib_id or str(), User.linkedin or str(),
        User.provider or str(), User.lattes_id or str()
    ])


def select_user(uid):
    SCRIPT_SQL = """
        SELECT u.user_id,
            display_name,
            email,
            uid,
            photo_url,
            shib_uid,
            jsonb_agg(jsonb_build_object('id', r.id, 'role_id', r.role)) AS roles,
            linkedin,
            provider,
            u.lattes_id,
            rr.institution_id,
            jsonb_agg(jsonb_build_object('graduate_program_id', gp.graduate_program_id, 'name', gp.name)) AS graduate_program
        FROM users u
        LEFT JOIN users_roles ur ON ur.user_id = u.user_id
        LEFT JOIN roles r ON r.id = ur.role_id
        LEFT JOIN researcher rr ON rr.lattes_id = u.lattes_id
        LEFT JOIN graduate_program_researcher gpr ON gpr.researcher_id = rr.researcher_id
        LEFT JOIN graduate_program gp ON gp.graduate_program_id = gpr.graduate_program_id
        WHERE uid = %s OR shib_uid = %s
        GROUP BY u.user_id, display_name, email, uid, photo_url, shib_uid, rr.institution_id;
        """
    print(SCRIPT_SQL)
    registry = adm_database.select(SCRIPT_SQL, [uid, uid])

    data_frame = pd.DataFrame(registry,
                              columns=[
                                  'user_id', 'display_name', 'email', 'uid',
                                  'photo_url', 'shib_uid', 'roles', 'linkedin',
                                  'provider', 'lattes_id', 'institution_id',
                                  'graduate_program'
                              ])

    return data_frame.to_dict(orient='records')


def update_user(user):
    SCRIPT_SQL = """
    UPDATE users
    SET linkedin = %s,
        lattes_id = %s,
        displayName = %s
    WHERE uid = %s
    """
    adm_database.exec(SCRIPT_SQL, [
        user['linkedin'], user['lattes_id'], user['display_name'], user['uid']
    ])


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


def create_new_permission(permission):
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
