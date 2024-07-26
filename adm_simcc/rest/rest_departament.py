from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..dao import dao_departament

rest_departament = Blueprint("rest_departament", __name__)


@rest_departament.route("/departamentos", methods=["POST"])
def departament_insert():
    departaments = request.form.to_dict()
    departaments_file = request.files
    dao_departament.departament_insert(departaments, departaments_file)
    return jsonify("OK"), HTTPStatus.CREATED


@rest_departament.route("/departamentos", methods=["GET"])
def departament_basic_query():
    departaments = dao_departament.departament_basic_query()
    return jsonify(departaments), HTTPStatus.OK
