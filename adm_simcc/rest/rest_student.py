import psycopg2
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_student
from ..models.student import ListStudent, Student


rest_student = Blueprint("rest_student", __name__, url_prefix="/studentRest")


@rest_student.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_insert():
    try:
        student_list = request.get_json()
        list_instance = ListStudent(student_list=student_list)
        dao_student.student_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "discente já cadastrado"}), HTTPStatus.CONFLICT


@rest_student.route("/update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_update():
    student = request.get_json()
    instance = Student(**student[0])
    dao_student.student_update(instance)
    return jsonify({"message": "ok"}), HTTPStatus.OK


@rest_student.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_delete():
    student = request.get_json()
    lattes_id = student[0]["lattes_id"]
    graduate_program_id = student[0]["graduate_program_id"]
    dao_student.student_delete(lattes_id, graduate_program_id)
    return jsonify(), HTTPStatus.NO_CONTENT


@rest_student.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_basic_query():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")
    students = dao_student.student_basic_query(graduate_program_id, institution_id)
    return jsonify(students), HTTPStatus.OK
