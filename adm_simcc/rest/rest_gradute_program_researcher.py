from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from http import HTTPStatus

from ..dao import dao_graduate_program_researcher
from ..models.graduate_program_resarcher import ListResearcher


rest_graduate_program_researcher = Blueprint(
    "rest_graduate_program_researcher",
    __name__,
    url_prefix="/graduateProgramResearcherRest",
)


@rest_graduate_program_researcher.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_insert():
    list_instance = request.get_json()
    researcher_instance = ListResearcher(researcher_list=list_instance)
    dao_graduate_program_researcher.graduate_program_researcher_insert(
        researcher_instance
    )
    return jsonify({"message": "ok"}), HTTPStatus.CREATED


@rest_graduate_program_researcher.route("/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_delete():
    researcher = request.get_json()
    researcher_id = researcher[0]["lattes_id"]
    graduate_program_id = researcher[0]["graduate_program_id"]
    dao_graduate_program_researcher.graduate_program_researcher_delete(
        researcher_id, graduate_program_id
    )
    return jsonify(), HTTPStatus.NO_CONTENT


@rest_graduate_program_researcher.route("/Query", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_basic_query():
    graduate_program_id = request.args.get("graduate_program_id")
    type_ = request.args.get("type")
    researchers = (
        dao_graduate_program_researcher.graduate_program_researcher_basic_query(
            graduate_program_id, type_
        )
    )
    return jsonify(researchers), HTTPStatus.OK


@rest_graduate_program_researcher.route("/Query/Count", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_count():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")
    researchers_count = (
        dao_graduate_program_researcher.graduate_program_researcher_count(
            institution_id, graduate_program_id
        )
    )
    return jsonify(researchers_count), HTTPStatus.OK
