from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_graduate_program
from ..models.graduate_program import GraduateProgram

rest_graduate_program = Blueprint(
    "rest_graduate_program", __name__, url_prefix="/graduateProgramRest"
)


@rest_graduate_program.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_insert():
    jsonGraduateProgram = request.get_json()
    if jsonGraduateProgram:
        for graduate_program in jsonGraduateProgram:
            dao_graduate_program.graduate_program_insert(
                GraduateProgram(**graduate_program)
            )
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program.route("/update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_update():
    graduate_program_id = request.args.get("graduate_program_id")
    if graduate_program_id:
        dao_graduate_program.graduate_program_update(graduate_program_id)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program.route("/fix", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_fix():
    jsonGraduateProgram = request.get_json()
    if jsonGraduateProgram:
        for graduate_program in jsonGraduateProgram:
            graduate_program_instance = GraduateProgram(**graduate_program)
            dao_graduate_program.graduate_program_fix(graduate_program_instance)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_delete():
    graduate_program_id = request.args.get("graduate_program_id")
    if graduate_program_id:
        dao_graduate_program.graduate_program_delete(graduate_program_id)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_basic_query():
    institution_id = request.args.get("institution_id")
    if institution_id:
        graduate_programs = dao_graduate_program.graduate_program_basic_query(
            institution_id
        )
        print(graduate_programs)
        return jsonify(graduate_programs)
    return jsonify(400, "bad request")


@rest_graduate_program.route("/query/count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_count():
    institution_id = request.args.get("institution_id")
    if institution_id:
        graduate_program_count = dao_graduate_program.graduate_program_count(
            institution_id
        )
        return jsonify(graduate_program_count)
    return jsonify(400, "bad request")
