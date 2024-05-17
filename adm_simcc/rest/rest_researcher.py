from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_researcher
from ..models.researcher import ListResearchers

from pydantic import ValidationError, UUID4
from http import HTTPStatus
from psycopg2 import Error

rest_researcher = Blueprint("rest_researcher", __name__, url_prefix="/ResearcherRest")


@rest_researcher.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert():
    researcher_list = request.get_json()
    try:
        list_instance = ListResearchers(researcher_list=researcher_list)
        dao_researcher.researcher_insert(list_instance)
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


@rest_researcher.route("/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_delete():
    researcher_id = request.args.get("researcher_id")
    try:
        researcher_id = UUID4(researcher_id)
        dao_researcher.researcher_delete(researcher_id)
        return jsonify(), HTTPStatus.NO_CONTENT
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


@rest_researcher.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    researcher_name = request.args.get("name")
    rows = request.args.get("count")
    try:
        researchers = dao_researcher.researcher_basic_query(
            institution_id, researcher_name, rows
        )
        return jsonify(researchers)
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_researcher.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_count():
    institution_id = request.args.get("institution_id")
    try:
        researchers_count = dao_researcher.researcher_count(institution_id)
        return jsonify(researchers_count)
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
