from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from http import HTTPStatus

from ..dao import dao_researcher
from ..models.researcher import ListResearchers


rest_researcher = Blueprint("rest_researcher", __name__, url_prefix="/ResearcherRest")


@rest_researcher.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def researcher_insert():
    researcher_list = request.get_json()
    list_instance = ListResearchers(researcher_list=researcher_list)
    response = dao_researcher.researcher_insert(list_instance)
    if response == 200:
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    if response == 400:
        return (
            jsonify({"message": "Entidade ja cadastrada no banco"}),
            HTTPStatus.BAD_REQUEST,
        )


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
