from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from Dao import indProdSQL

ind_prod = Blueprint("ind_prod", __name__)


@ind_prod.route("/indProd", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def indProd():
    weights = request.get_json()

    indProdSQL.calc_ind_prod(weights)
    return jsonify(200, "ok")
