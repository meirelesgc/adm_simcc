from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_graduate_program_researcher
from ..models.graduate_program_resarcher import GraduateProgramResearcher

rest_graduate_program_researcher = Blueprint(
    "rest_graduate_program_researcher",
    __name__,
    url_prefix="/graduateProgramResearcherRest",
)


@rest_graduate_program_researcher.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_insert():
    jsonResearcher = request.get_json()
    for researcher in jsonResearcher:
        researcher_instance = GraduateProgramResearcher(**researcher)
        dao_graduate_program_researcher.graduate_program_researcher_insert(
            researcher_instance
        )
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program_researcher.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_delete():
    researcher_id = request.args.get("researcher_id")
    graduate_program_id = request.args.get("graduate_program_id")

    if researcher_id and graduate_program_id:
        dao_graduate_program_researcher.graduate_program_researcher_delete(
            researcher_id, graduate_program_id
        )
        return jsonify(200, "ok")
    elif researcher := request.get_json():
        dao_graduate_program_researcher.graduate_program_researcher_delete(
            researcher["lattes_id"], researcher["graduate_program_id"]
        )
        return jsonify(200, "ok")
    return jsonify(400, "bad request")


@rest_graduate_program_researcher.route("/query", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_basic_query():
    graduate_program_id = request.args.get("graduate_program_id")
    type_ = request.args.get("type")
    jsonResearchers = (
        dao_graduate_program_researcher.graduate_program_researcher_basic_query(
            graduate_program_id, type_
        )
    )
    return jsonify(jsonResearchers), 200


@rest_graduate_program_researcher.route("/query/count", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def graduate_program_researcher_count():
    institution_id = request.args.get("institution_id")
    graduate_program_id = request.args.get("graduate_program_id")
    if institution_id or graduate_program_id:
        researchers_count = (
            dao_graduate_program_researcher.graduate_program_researcher_count(
                institution_id, graduate_program_id
            )
        )
        return jsonify(researchers_count)
    return jsonify(400, "bad request")
