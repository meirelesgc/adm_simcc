from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from ..dao import dao_system

rest_sys = Blueprint("rest_system_management", __name__, url_prefix="/sys")


@rest_sys.route("/checkHop", methods=["GET"])
def checkHop():
    line = dao_system.check_load()
    return jsonify({"message": line}), HTTPStatus.OK


@rest_sys.route("/requestUpdate", methods=["POST"])
def requestUpdate():
    onHop = request.get_json()
    if onHop[0]["state"]:
        dao_system.request_load(onHop[0]["institution_id"])
        return jsonify({"message": "Carga solicitada!"}), HTTPStatus.OK
