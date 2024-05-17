from flask import Blueprint, jsonify, request
from flask_cors import cross_origin


from ..dao import dao_institution
from ..models.institution import ListInstitutions

from http import HTTPStatus
from pydantic import ValidationError
from psycopg2 import Error

rest_institution = Blueprint(
    "rest_institution", __name__, url_prefix="/InstitutionRest"
)


@rest_institution.route("/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def institution_insert():
    list_institutions = request.get_json()
    try:
        list_instance = ListInstitutions(institution_list=list_institutions)
        dao_institution.institution_insert(list_instance)
        return jsonify({"message": "ok"}), HTTPStatus.CREATED
    except ValidationError as E:
        return jsonify({"message": str(E)}), HTTPStatus.BAD_REQUEST
    except Error as E:
        return (
            jsonify({"message":  str(E)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
    except Exception as E:
        return (
            jsonify({"message": str(E)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_institution.route("/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def basic_query():
    institution_id = request.args.get("institution_id")
    try:
        institutions = dao_institution.institution_basic_query(institution_id)
        return jsonify(institutions), HTTPStatus.OK
    except ValueError as erro:
        return jsonify({"message": str(erro)}), HTTPStatus.BAD_REQUEST
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@rest_institution.route("/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def full_query():

    institution_id = request.args.get("institution_id")

    try:
        institutions = dao_institution.institution_full_query(institution_id)
        return jsonify(institutions), HTTPStatus.OK
    except ValueError as erro:
        return jsonify({"message": str(erro)}), HTTPStatus.BAD_REQUEST
    except Exception:
        return (
            jsonify({"message": "Problema no banco"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
