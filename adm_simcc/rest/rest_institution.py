from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_institution
from ..models.institution import ListInstitutions


rest_institution = Blueprint(
    "rest_institution", __name__, url_prefix="/InstitutionRest"
)


@rest_institution.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def institution_insert():
    list_institutions = request.get_json()
    list_instance = ListInstitutions(institution_list=list_institutions)
    dao_institution.institution_insert(list_instance)
    return jsonify({"message": "ok"}), HTTPStatus.CREATED


@rest_institution.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def institution_basic_query():
    institution_id = request.args.get("institution_id")
    institutions = dao_institution.institution_basic_query(institution_id)
    return jsonify(institutions), HTTPStatus.OK


@rest_institution.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def institution_full_query():
    institution_id = request.args.get("institution_id")
    institutions = dao_institution.institution_full_query(institution_id)
    return jsonify(institutions), HTTPStatus.OK
