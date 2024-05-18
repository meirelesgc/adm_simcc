from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from pydantic import UUID4
from http import HTTPStatus

from ..dao import dao_researcher
from ..models.researcher import ListResearchers


rest_researcher = Blueprint(
    "rest_researcher", __name__, url_prefix="/ResearcherRest")


@rest_researcher.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert():
    researcher_list = request.get_json()
    list_instance = ListResearchers(researcher_list=researcher_list)
    dao_researcher.researcher_insert(list_instance)
    return jsonify({"message": "ok"}), HTTPStatus.CREATED


@rest_researcher.route("/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_delete():
    researcher_id = request.args.get("researcher_id")
    researcher_id = UUID4(researcher_id)
    dao_researcher.researcher_delete(researcher_id)
    return jsonify(), HTTPStatus.NO_CONTENT


@rest_researcher.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    researcher_name = request.args.get("name")
    rows = request.args.get("count")
    researchers = dao_researcher.researcher_basic_query(
        institution_id, researcher_name, rows
    )
    return jsonify(researchers)


@rest_researcher.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_count():
    institution_id = request.args.get("institution_id")
    researchers_count = dao_researcher.researcher_count(institution_id)
    return jsonify(researchers_count)
