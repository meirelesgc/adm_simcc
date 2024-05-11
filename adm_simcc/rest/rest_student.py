from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_student
from ..models.student import Student

rest_student = Blueprint("rest_student", __name__, url_prefix="/studentRest")


@rest_student.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_insert():
    jsonStudents = request.get_json()
    print(jsonStudents)
    if jsonStudents:
        for student in jsonStudents:
            student = Student(**student)
            dao_student.student_insert(student)
        return jsonify("OK"), 200
    return jsonify(400, "bad request")


@rest_student.route("/update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_update():
    student = request.get_json()
    if student:
        student = Student(**student)
        dao_student.student_insert(student)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_student.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_delete():
    student_id = request.args.get("student_id")
    dao_student.student_delete(student_id)
    return jsonify(200, "ok")


@rest_student.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_basic_query():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")
    if institution_id or graduate_program_id:
        jsonStudents = dao_student.student_basic_query(
            graduate_program_id, institution_id
        )
        return jsonify(jsonStudents)
    return jsonify(400, "bad request")
