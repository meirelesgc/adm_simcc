import psycopg2
from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..dao import dao_technician
from ..models.technician import ListTechnician

rest_technician = Blueprint("rest_technician", __name__)


@rest_technician.route("/tecnicos", methods=["POST"])
def technician_insert():
    try:
        technician = request.get_json()
        technician = ListTechnician(list_technician=technician)
        dao_technician.technician_insert(technician)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "Tecnico já cadastrado"}), HTTPStatus.CONFLICT


@rest_technician.route("/tecnicos", methods=["GET"])
def technician_basic_query():
    year = request.args.get("year")
    semester = request.args.get("semester")
    departament = request.args.get("departament")
    technicians = dao_technician.technician_basic_query(year, semester, departament)
    return jsonify(technicians), HTTPStatus.OK
