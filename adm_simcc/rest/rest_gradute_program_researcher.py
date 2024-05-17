import json
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_graduate_program_researcher
from ..models.graduate_program_resarcher import ListResearcher

from pydantic import ValidationError
from http import HTTPStatus
from psycopg2 import Error

rest_graduate_program_researcher = Blueprint(
    "rest_graduate_program_researcher",
    __name__,
    url_prefix="/graduateProgramResearcherRest",
)


@rest_graduate_program_researcher.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_insert():
    list_instance = request.get_json()
    print(list_instance)
    try:
        researcher_instance = ListResearcher(researcher_list=list_instance)
        dao_graduate_program_researcher.graduate_program_researcher_insert(
            researcher_instance
        )
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


@rest_graduate_program_researcher.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_delete():
    researcher = request.get_json()
    try:
        researcher_id = researcher[0]["lattes_id"]
        graduate_program_id = researcher[0]["graduate_program_id"]
        dao_graduate_program_researcher.graduate_program_researcher_delete(
            researcher_id, graduate_program_id
        )
        return jsonify(), HTTPStatus.NO_CONTENT
    except Exception:
        return (
            jsonify({"message": f"Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program_researcher.route("/query", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_basic_query():
    graduate_program_id = request.args.get("graduate_program_id")
    type_ = request.args.get("type")
    try:
        researchers = (
            dao_graduate_program_researcher.graduate_program_researcher_basic_query(
                graduate_program_id, type_
            )
        )
        return jsonify(researchers), HTTPStatus.OK
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_graduate_program_researcher.route("/query/count", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_count():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")
    try:
        researchers_count = (
            dao_graduate_program_researcher.graduate_program_researcher_count(
                institution_id, graduate_program_id
            )
        )
        return jsonify(researchers_count), HTTPStatus.OK
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
