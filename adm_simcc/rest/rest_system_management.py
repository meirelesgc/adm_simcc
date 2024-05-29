from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import os
import subprocess

rest_sys = Blueprint("rest_system_management", __name__, url_prefix="/sys")


@rest_sys.route("/requestUpdate", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def requestUpdate():
    with open(os.environ["HOP_LOG_PATH"], "r") as archive:
        if line := archive.readlines():
            return jsonify({"message": line[-1].strip()}), HTTPStatus.OK
        else:
            subprocess.Popen(
                [
                    "/home/ejorge/hop/hop-run.sh",
                    "-r",
                    "local",
                    "-j",
                    "Jade-Extrator-Hop",
                    "-f",
                    "${PROJECT_HOME}/metadata/dataset/workflow/ImportGraduation.hwf",
                ],
                shell=True,
            )
            return (
                jsonify({"message": "A carga dos pesquisadores começou!"}),
                HTTPStatus.OK,
            )
