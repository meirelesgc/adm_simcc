import os
import subprocess

from http import HTTPStatus
from flask import Blueprint, jsonify
from flask_cors import cross_origin

rest_sys = Blueprint("rest_system_management", __name__, url_prefix="/sys")


@rest_sys.route("/requestUpdate", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def requestUpdate():
    if line := read_log(os.environ["HOP_LOG_PATH"]):
        return jsonify({"message": line}), HTTPStatus.OK
    else:
        subprocess.Popen(["/usr/local/sbin/Jade-Extrator-Routine.sh",],shell=True,)  # fmt: skip
        return jsonify({"message": "processo de carga iniciado"}), HTTPStatus.OK


def read_log(path):
    with open(path, "r", encoding="utf-8") as archive:
        lines = archive.readlines()
        if lines:
            return lines[-1].strip()
        else:
            return None
