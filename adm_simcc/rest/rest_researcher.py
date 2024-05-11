from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_researcher
from ..models.researcher import Researcher

rest_researcher = Blueprint("rest_researcher", __name__, url_prefix="/researcherRest")


@rest_researcher.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert():
    jsonResearchers = request.get_json()
    if jsonResearchers:
        for researcher in jsonResearchers:
            researcher_instance = Researcher(**researcher)
            dao_researcher.researcher_insert(researcher_instance)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_researcher.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_delete():
    researcher_id = request.args.get("researcher_id")
    if researcher_id:
        dao_researcher.researcher_delete(researcher_id)
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_researcher.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    if institution_id:
        researchers = dao_researcher.researcher_basic_query(institution_id)
        return jsonify(researchers)
    return jsonify(400, "bad request")


@rest_researcher.route("/query/count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_count():
    institution_id = request.args.get("institution_id")
    if institution_id:
        researchers_count = dao_researcher.researcher_count(institution_id)
        return jsonify(researchers_count)
    return jsonify(400, "bad request")
