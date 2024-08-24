import psycopg2
from http import HTTPStatus
from flask import Blueprint, jsonify, request

from ..dao import dao_researcher
from ..models.researcher import (
    ListResearchers,
    ListSubsidies,
    Subsidies,
    ListResearcherDepartament,
)


rest_researcher = Blueprint("rest_researcher", __name__, url_prefix="/ResearcherRest")


@rest_researcher.route("/Insert", methods=["POST"])
def researcher_insert():
    try:
        researcher_list = request.get_json()
        list_instance = ListResearchers(researcher_list=researcher_list)
        dao_researcher.researcher_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "pesquisador ja cadastrado"}), HTTPStatus.CONFLICT


@rest_researcher.route("/Delete", methods=["DELETE"])
def researcher_delete():
    researcher_id = request.args.get("researcher_id")
    dao_researcher.researcher_delete(researcher_id)
    return jsonify(), HTTPStatus.NO_CONTENT


@rest_researcher.route("/Query", methods=["GET"])
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
def researcher_count():
    institution_id = request.args.get("institution_id")
    researchers_count = dao_researcher.researcher_count(institution_id)
    return jsonify(researchers_count)


@rest_researcher.route("/InsertGrant", methods=["POST"])
def researcher_insert_grant():
    grant_list = request.get_json()
    for a, b in enumerate(grant_list):
        try:
            Subsidies(**b)
        except Exception as E:
            print(b, E)
    list_instance = ListSubsidies(grant_list=grant_list)
    print("cheguei até aqui")
    untracket_researchers = dao_researcher.researcher_insert_grant(list_instance)
    return jsonify({"not found": untracket_researchers}), HTTPStatus.CREATED


@rest_researcher.route("/Query/Subsidy", methods=["GET"])
def researcher_query_grant():
    institution_id = request.args.get("institution_id")
    researchers_list = dao_researcher.researcher_query_grant(institution_id)
    return jsonify(researchers_list), HTTPStatus.OK


@rest_researcher.route("/departament", methods=["POST"])
def researcher_departament_insert():
    try:
        researchers = request.get_json()
        researchers = ListResearcherDepartament(researcher_departament=researchers)
        dao_researcher.researcher_departament_insert(researchers)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except psycopg2.errors.UniqueViolation:
        return (
            jsonify({"message": "pesquisador ja cadastrado neste departamento"}),
            HTTPStatus.CONFLICT,
        )


@rest_researcher.route("/departament", methods=["DELETE"])
def researcher_departament_delete():
    researcher = request.get_json()
    dao_researcher.researcher_departament_delete(researcher)
    return jsonify({"message": "ok"}), HTTPStatus.NO_CONTENT


@rest_researcher.route("/departament", methods=["GET"])
def researcher_departament_basic_query():
    researcher_id = request.args.get("researcher_id")

    researchers = dao_researcher.researcher_departament_basic_query(
        researcher_id)
    return jsonify(researchers), HTTPStatus.OK
