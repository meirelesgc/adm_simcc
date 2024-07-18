from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..dao import dao_departament

rest_departament = Blueprint("rest_departament", __name__)


@rest_departament.route("/departamento", methods=["POST"])
def departament_insert():
    departaments = request.get_json()
    departaments_file = request.files
    dao_departament.departament_insert(departaments, departaments_file)
    return jsonify("OK"), HTTPStatus.CREATED


@rest_departament.route("/departamento", methods=["GET"])
def departament_basic_query():
    return dao_departament.departament_basic_query(), HTTPStatus.OK
