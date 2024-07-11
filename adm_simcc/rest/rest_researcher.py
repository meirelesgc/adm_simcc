import psycopg2
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_researcher
from ..models.researcher import ListResearchers, ListSubsidies


rest_researcher = Blueprint("rest_researcher", __name__, url_prefix="/ResearcherRest")


@rest_researcher.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert():
    try:
        researcher_list = request.get_json()
        list_instance = ListResearchers(researcher_list=researcher_list)
        dao_researcher.researcher_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "pesquisador ja cadastrado"}), HTTPStatus.CONFLICT


@rest_researcher.route("/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_delete():
    researcher_id = request.args.get("researcher_id")
    dao_researcher.researcher_delete(researcher_id)
    return jsonify(), HTTPStatus.NO_CONTENT


@rest_researcher.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_basic_query():
    institution_id = request.args.get("institution_id")
    researcher_name = request.args.get("name")
    rows = request.args.get("count")
    lattes_id = request.args.get("lattes_id")

    researchers = dao_researcher.researcher_basic_query(
        institution_id=institution_id,
        researcher_name=researcher_name,
        rows=rows,
        lattes_id=lattes_id,
    )
    return jsonify(researchers), HTTPStatus.OK


@rest_researcher.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_count():
    institution_id = request.args.get("institution_id")
    researchers_count = dao_researcher.researcher_count(institution_id)
    return jsonify(researchers_count)


@rest_researcher.route("/InsertGrant", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert_grant():
    grant_list = request.get_json()
    list_instance = ListSubsidies(grant_list=grant_list)
    untracket_researchers = dao_researcher.researcher_insert_grant(list_instance)
    return jsonify({"not found": untracket_researchers}), HTTPStatus.CREATED


@rest_researcher.route("/Query/Subsidy", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_query_grant():
    institution_id = request.args.get("institution_id")
    researchers_list = dao_researcher.researcher_query_grant(institution_id)
    return jsonify(researchers_list), HTTPStatus.OK
