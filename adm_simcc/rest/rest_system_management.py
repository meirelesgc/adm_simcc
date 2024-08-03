from http import HTTPStatus
from flask import Blueprint, jsonify, request
import os
import json
from ..dao import dao_system

rest_system = Blueprint("rest_system_management", __name__)


@rest_system.route('/api/save-directory', methods=['POST'])
def save_directory():
    data = request.json
    directory = data.get('directory')

    if not directory:
        return jsonify({'error': 'No directory provided'}), 400

    file_path = os.path.join(os.path.dirname(__file__), 'directory.json')

    try:
        with open(file_path, 'w') as file:
            json.dump({'directory': directory}, file)
        return jsonify({'message': 'Directory saved successfully'}), 200
    except Exception as e:
        print('Error saving directory:', e)
        return jsonify({'error': 'Failed to save directory'}), 500


@rest_system.route('/api/directory', methods=['GET'])
def get_directory():
    file_path = os.path.join(os.path.dirname(__file__), 'directory.json')

    try:
        with open(file_path, 'r') as file:
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
def delete_roles():
    role = request.get_json()
    dao_system.delete_roles(role)
    return jsonify(), HTTPStatus.OK