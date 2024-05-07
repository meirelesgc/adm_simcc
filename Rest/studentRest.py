from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from Dao import StudentSQL
from Model.Student import Student

studentRest = Blueprint("studentRest", __name__)


@studentRest.route("/studentRest/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def insert():
    jsonStudents = request.get_json()
    if jsonStudents:
        for student in jsonStudents:
            student_instance = Student(**student)
            StudentSQL.insert(student=student_instance)
    return jsonify("OK"), 200


@studentRest.route("/studentRest/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")

    jsonStudents = StudentSQL.query(graduate_program_id, institution_id)
    print(jsonStudents)
    return jsonify(jsonStudents)


@studentRest.route("/studentRest/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def delete():
    student_id = request.args.get("student_id")
    StudentSQL.delete(student_id)
    return jsonify(200, "ok")


@studentRest.route("/studentRest/update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def update():
    student = request.get_json()
    student_instance = Student(**student)
    StudentSQL.update(student_instance)
    return jsonify(200, "ok")
