import os
import json
import psycopg2

from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..dao import dao_system
from ..models import UserModel

rest_system = Blueprint("rest_system_management", __name__)


@rest_system.route('/s/user', methods=['POST'])
def create_user():
    try:
        user = request.get_json()
        user = UserModel(**user[0])
        dao_system.create_user(user)
        return jsonify('OK'), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "discente já cadastrado"}), HTTPStatus.OK

@rest_system.route('/s/user', methods=['GET'])
def select_user():
    uid = request.args.get('uid')
    user = dao_system.select_user(uid)
    return jsonify(user), HTTPStatus.OK


@rest_system.route('/s/user', methods=['PUT'])
def update_user():
    user = request.get_json()
    dao_system.update_user(user[0])
    return jsonify(), HTTPStatus.OK


@rest_system.route('/s/save-directory', methods=['POST'])
def save_directory():
    data = request.json
    directory = data.get('directory')

    if not directory:
        return jsonify({'error': 'No directory provided'}), 400

    try:
        with open('files/directory.json', 'w') as file:
            json.dump({'directory': directory}, file)
        return jsonify({'message': 'Directory saved successfully'}), 200
    except Exception as e:
        print('Error saving directory:', e)
        return jsonify({'error': 'Failed to save directory'}), 500


@rest_system.route('/s/directory', methods=['GET'])
def get_directory():

    try:
        with open('files/directory.json', 'r') as file:
            data = json.load(file)
            directory_path = data.get('directory')
        if not directory_path:
            return jsonify({'error': 'Directory path not found'}), 404

        directory_list = os.listdir(directory_path)
        return jsonify(directory_list)
    except FileNotFoundError:
        return jsonify({'error': 'Directory file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@rest_system.route('/s/role', methods=['POST'])
def create_new_role():
    role = request.get_json()
    dao_system.create_new_role(role)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/role', methods=['GET'])
def view_roles():
    roles = dao_system.view_roles()
    return jsonify(roles), HTTPStatus.OK


@rest_system.route('/s/role', methods=['PUT'])
def update_role():
    role = request.get_json()
    dao_system.update_role(role)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/role', methods=['DELETE'])
def delete_role():
    role = request.get_json()
    dao_system.delete_role(role)
    return jsonify(), HTTPStatus.OK


@rest_system.route('/s/permission', methods=['POST'])
def create_new_permission():
    permission = request.get_json()
    dao_system.create_new_permission(permission)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/permission', methods=['GET'])
def permissions_view():
    role_id = request.args.get('role_id')
    roles = dao_system.permissions_view(role_id)
    return jsonify(roles), HTTPStatus.OK



@rest_system.route('/s/permission', methods=['PUT'])
def update_permission():
    permission = request.get_json()
    dao_system.update_permission(permission)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/permission', methods=['DELETE'])
def delete_permission():
    permission = request.get_json()
    dao_system.delete_permission(permission)
    return jsonify('OK'), HTTPStatus.NO_CONTENT


@rest_system.route('/s/researcher/role', methods=['POST'])
def assign_researcher():
    researcher = request.get_json()
    dao_system.assign_researcher(researcher)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/researcher/role', methods=['GET'])
def view_researcher_roles():
    dao_system.view_researcher_roles()
    return jsonify('OK'), HTTPStatus.OK


@rest_system.route('/s/researcher/role', methods=['DELETE'])
def unassign_researcher():
    researcher = request.get_json()
    dao_system.unassign_researcher(researcher)
    return jsonify('OK'), HTTPStatus.NO_CONTENT


@rest_system.route('/s/technician/role', methods=['POST'])
def assign_technician():
    technician = request.get_json()
    dao_system.assign_technician(technician)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/technician/role', methods=['GET'])
def view_technician_roles():
    dao_system.view_technician_roles()
    return jsonify('OK'), HTTPStatus.OK


@rest_system.route('/s/technician/role', methods=['DELETE'])
def unassign_technician():
    technician = request.get_json()
    dao_system.unassign_technician(technician)
    return jsonify('OK'), HTTPStatus.NO_CONTENT


@rest_system.route('/s/user/role', methods=['POST'])
def assign_user():
    user = request.get_json()
    dao_system.assign_user(user)
    return jsonify('OK'), HTTPStatus.CREATED


@rest_system.route('/s/user/role', methods=['GET'])
def view_user_roles():
    dao_system.view_user_roles()
    return jsonify('OK'), HTTPStatus.OK


@rest_system.route('/s/user/role', methods=['DELETE'])
def unassign_user():
    technician = request.get_json()
    dao_system.unassign_user(technician)
    return jsonify('OK'), HTTPStatus.NO_CONTENT
