from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_institution
from ..models.institution import Institution

rest_institution = Blueprint(
    "rest_institution", __name__, url_prefix="/institutionRest"
)


@rest_institution.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def institution_insert():
    jsonInstitutions = request.get_json()
    if jsonInstitutions:
        for institution in jsonInstitutions:
            dao_institution.institution_insert(Institution(**institution))
        return jsonify(200, "ok")
    return jsonify(209, "conflict")


@rest_institution.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    if institution_id:
        institution = dao_institution.institution_basic_query(institution_id)
        return jsonify(institution)
    return jsonify(400, "bad request")


@rest_institution.route("/query/count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def full_query():
    institution_id = request.args.get("institution_id")
    institutions = dao_institution.institution_full_query(institution_id)
    return jsonify(institutions)
