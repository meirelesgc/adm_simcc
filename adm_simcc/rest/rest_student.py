from ast import List
from csv import excel
from uuid import UUID
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_student
from ..models.student import ListStudent, Student

from pydantic import ValidationError, UUID4
from http import HTTPStatus
from psycopg2 import Error

rest_student = Blueprint("rest_student", __name__, url_prefix="/studentRest")


@rest_student.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_insert():
    student_list = request.get_json()
    try:
        list_instance = ListStudent(student_list=student_list)
        dao_student.student_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except Error:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception:
        return (
            jsonify({"message": "Problema não mapeado"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_student.route("/update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_update():
    student = request.get_json()
    try:
        instance = Student(**student[0])
        dao_student.student_update(instance)
        return jsonify({"message": "ok"}), HTTPStatus.OK
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except Error:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception:
        return (
            jsonify({"message": "Problema não mapeado"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_student.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_delete():
    student_id = request.args.get("student_id")
    try:
        student_id = UUID4(student_id)
        dao_student.student_delete(student_id)
        return jsonify(), HTTPStatus.NO_CONTENT
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except Error:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_student.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def student_basic_query():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")

    try:
        students = dao_student.student_basic_query(graduate_program_id, institution_id)
        return jsonify(students), HTTPStatus.OK
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
