from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import os
import json
from ..dao import dao_system

rest_sys = Blueprint("rest_system_management", __name__)


@rest_sys.route('/api/save-directory', methods=['POST'])
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
    

@rest_sys.route('/api/directory', methods=['GET'])
def get_directory():
    # Define the path to the file where the directory is saved
    file_path = os.path.join(os.path.dirname(__file__), 'directory.json')

    try:
        # Read the directory path from the file
        with open(file_path, 'r') as file:
            data = json.load(file)
            directory_path = data.get('directory')

        if not directory_path:
            return jsonify({'error': 'Directory path not found'}), 404

        # Get the directory listing
        directory_list = os.listdir(directory_path)

        # Return the directory listing as JSON
        return jsonify(directory_list)
    except FileNotFoundError:
        return jsonify({'error': 'Directory file not found'}), 404
    except Exception as e:
        # Handle errors (e.g., invalid directory path)
        return jsonify({'error': str(e)}), 500