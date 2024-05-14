from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from Dao import ResearcherSQL
from Model.Resercher import Researcher

researcherRest = Blueprint("researcherRest", __name__)


@researcherRest.route("/ResearcherRest/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def query_table():
    JsonResearchers = list()
    
    instituion_id = request.args.get("institution_id")
    researcher_name = request.args.get('name')
    limit = request.args.get('count')
    dfResearcher = ResearcherSQL.Query(instituion_id, researcher_name, limit)

    for Index, researcher in dfResearcher.iterrows():
        researcher_inst = Researcher()
        researcher_inst.researcher_id = researcher["researcher_id"]
        researcher_inst.name = researcher["name"]
        researcher_inst.lattes_id = researcher["lattes_id"]
        researcher_inst.institution_id = researcher["institution_id"]

        JsonResearchers.append(researcher_inst.get_json())

    return jsonify(JsonResearchers), 200


@researcherRest.route("/ResearcherRest/Query/Count", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def query_count():
    count = ResearcherSQL.query_count()
    return jsonify(count), 200


@researcherRest.route("/ResearcherRest/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def Insert():
    JsonInstitutions = request.get_json()

    if not JsonInstitutions:
        return jsonify({"https://github.com/ovictorhugo/sistema-de-mapeamento-de-competencias.giterror": "Erro no Json enviado"}), 400

    try:
        for researcher_data in JsonInstitutions:
            researcher_inst = Researcher()
            researcher_inst.researcher_id = researcher_data["researcher_id"]
            researcher_inst.name = researcher_data["name"]
            researcher_inst.lattes_id = researcher_data["lattes_id"]
            researcher_inst.institution_id = researcher_data["institution_id"]

            ResearcherSQL.Insert(researcher_inst)
    except Exception as Error:
        return jsonify(f"{Error}"), 400

    return jsonify("OK"), 200


@researcherRest.route("/ResearcherRest/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def Delete():
    ResearcherSQL.Delete(request.args.get("researcher_id"))
    return jsonify("OK"), 200
