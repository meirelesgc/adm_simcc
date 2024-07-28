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
    dep_id = request.args.get("dep_id")
    departaments = dao_departament.departament_basic_query(dep_id)
    return jsonify(departaments), HTTPStatus.OK


@rest_departament.route("/departamentos", methods=["DELETE"])
def departament_delete():
    dep_id = request.args.get("dep_id")
    dao_departament.departament_delete(dep_id)
    return jsonify("OK"), HTTPStatus.NO_CONTENT


@rest_departament.route("/departamentos/update", methods=["POST"])
def departament_update():
    departament = request.form.to_dict()
    departaments_file = request.files
    dao_departament.departament_update(departament, departaments_file)
    return jsonify("OK"), HTTPStatus.OK


@rest_departament.route("/departamentos/researcher", methods=["GET"])
def departament_researcher_query():
    dep_id = request.args.get("dep_id")
    researchers = dao_departament.departament_researcher_query(dep_id)
    return jsonify(researchers), HTTPStatus.OK
