import os
import subprocess

from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

rest_sys = Blueprint("rest_system_management", __name__, url_prefix="/sys")


@rest_sys.route("/checkHop", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def checkHop():
    line = read_log(os.environ["HOP_LOG_PATH"])
    if line and line != "ok":
        return jsonify({"message": line}), HTTPStatus.OK
    else:
        return jsonify({"message": "hop em modo de espera"}), HTTPStatus.OK


@rest_sys.route("/requestUpdate", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def requestUpdate():
    onHop = request.get_json()
    line = read_log(os.environ["HOP_LOG_PATH"])
    if line and line != "ok":
        return jsonify({"message": "hop em uso"}), HTTPStatus.OK
    elif onHop[0]["state"]:
        subprocess.Popen(["/usr/local/sbin/Jade-Extrator-Routine-Testes.sh",],shell=True,)  # fmt: skip
        return jsonify({"message": "processo de carga iniciado"}), HTTPStatus.OK


def read_log(path):
    with open(path, "r", encoding="utf-8") as archive:
        lines = archive.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return None
