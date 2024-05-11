from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from Dao import indProdSQL
from Model.weights import Weights

ind_prod = Blueprint("ind_prod", __name__, url_prefix="/indprod")


@ind_prod.route("/insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_insert():
    weights_list = request.get_json()
    if weights_list:
        for weights in weights_list:
            indProdSQL.insert_ind_prod(Weights(**weights))
        return jsonify(200, "ok")


@ind_prod.route("/delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_delete():
    weight_id = request.args.get("weight_id")
    indProdSQL.ind_prod_delete(weight_id)
    return jsonify(200, "ok")


@ind_prod.route("/query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def ind_prod_basic_query():
    institution_id = request.args.get("institution_id")
    jsonWeights = indProdSQL.ind_prod_basic_query(institution_id)
    return jsonify(jsonWeights)
