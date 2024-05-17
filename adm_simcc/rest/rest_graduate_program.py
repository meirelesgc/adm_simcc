import json
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_graduate_program
from ..models.graduate_program import GraduateProgram, ListGraduateProgram

from http import HTTPStatus
from pydantic import ValidationError, UUID4
from psycopg2 import Error, IntegrityError

from adm_simcc.models import graduate_program

rest_graduate_program = Blueprint(
    "rest_graduate_program", __name__, url_prefix="/graduateProgramRest"
)


@rest_graduate_program.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_insert():
    graduate_program_list = request.get_json()
    try:
        list_instance = ListGraduateProgram(graduate_program_list=graduate_program_list)
        dao_graduate_program.graduate_program_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return (
            jsonify({"message": "Violação de regras do banco de dados."}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except (Exception, Error):
        return (
            jsonify({"message": "Problema não mapeado"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program.route("/Update", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_update():
    graduate_program_id = request.args.get("graduate_program_id")
    try:
        graduate_program_id = UUID4(graduate_program_id)
        dao_graduate_program.graduate_program_update(graduate_program_id)
        return jsonify("message", "ok"), HTTPStatus.OK
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return (
            jsonify({"message": "Violação de regras do banco de dados."}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except (Exception, Error):
        return (
            jsonify({"message": "Problema na api"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program.route("/Fix", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_fix():
    graduate_program = request.get_json()
    try:
        instance = GraduateProgram(**graduate_program[0])
        dao_graduate_program.graduate_program_fix(instance)
        return jsonify({"message": "ok"}), HTTPStatus.OK
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return (
            jsonify(
                {"message": "Violação das regras de integridade do banco de dados."}
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except (Exception, Error):
        return (
            jsonify({"message": "Problema não mapeado"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program.route("/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_delete():
    graduate_program_id = request.args.get("graduate_program_id")
    try:
        graduate_program_id = UUID4(graduate_program_id)
        dao_graduate_program.graduate_program_delete(graduate_program_id)
        return jsonify(), HTTPStatus.NO_CONTENT
    except ValueError as erro:
        return jsonify({"message": str(erro)}), HTTPStatus.BAD_REQUEST
    except Exception as erro:
        return (
            jsonify({"message": "Problema não mapeado"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_basic_query():
    institution_id = request.args.get("institution_id")
    try:
        graduate_programs = dao_graduate_program.graduate_program_basic_query(
            institution_id
        )
        return jsonify(graduate_programs), HTTPStatus.OK
    except ValueError as erro:
        return jsonify({"message": str(erro)}), HTTPStatus.BAD_REQUEST
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_count():
    institution_id = request.args.get("institution_id")
    try:
        graduate_program_count = dao_graduate_program.graduate_program_count(
            institution_id
        )
        return jsonify(graduate_program_count), HTTPStatus.OK
    except ValueError as erro:
        return jsonify({"message": str(erro)}), HTTPStatus.BAD_REQUEST
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
