from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_teacher
from ..models.teachers import ListTeachers

rest_teacher = Blueprint("rest_teacher", __name__)


@rest_teacher.route("/docentes", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def teacher_insert():
    teachers = request.get_json()
    print(teachers)
    teachers = ListTeachers(list_teachers=teachers)
    dao_teacher.teacher_insert(teachers)
    return jsonify({"message": "ok"}), HTTPStatus.CREATED


@rest_teacher.route("/docentes", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def teacher_query():
    year = request.args.get("year")
    semester = request.args.get("semester")
    teachers = dao_teacher.reacher_basic_query(year, semester)
    return jsonify(teachers)
