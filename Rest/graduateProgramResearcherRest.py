from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from Dao import GraduateProgramResearcherSQL
from Model.GraduateProgramResearcher import GraduateProgramResearcher

graduateProgramResearcherRest = Blueprint("graduateProgramResearcherRest", __name__)


@graduateProgramResearcherRest.route(
    "/GraduateProgramResearcherRest/Query", methods=["GET"]
)
@cross_origin(origin="*", headers=["Content-Type"])
def Query():
    graduate_program_id = request.args.get("graduate_program_id")
    type_ = request.args.get("type")

    jsonResearchers = GraduateProgramResearcherSQL.query(graduate_program_id, type_)
    return jsonify(jsonResearchers), 200


@graduateProgramResearcherRest.route(
    "/GraduateProgramResearcherRest/Insert", methods=["POST"]
)
@cross_origin(origin="*", headers=["Content-Type"])
def Insert():
    JsonGpResearcher = request.get_json()
    if not JsonGpResearcher:
        return jsonify({"error": "Erro no Json enviado"}), 400
    try:
        for GpResearcher_data in JsonGpResearcher:
            gp_researcher_inst = GraduateProgramResearcher()
            gp_researcher_inst.graduate_program_id = GpResearcher_data[
                "graduate_program_id"
            ]
            gp_researcher_inst.lattes_id = GpResearcher_data["lattes_id"]
            gp_researcher_inst.year = GpResearcher_data["year"]
            gp_researcher_inst.type_ = GpResearcher_data["type_"]

            GraduateProgramResearcherSQL.insert(gp_researcher_inst)
    except Exception as Error:
        return jsonify(f"{Error}"), 400

    return jsonify("Incerssão bem sucedida"), 200


@graduateProgramResearcherRest.route(
    "/GraduateProgramResearcherRest/Delete", methods=["DELETE"]
)
@cross_origin(origin="*", headers=["Content-Type"])
def Delete():

    researcher = request.get_json()
    print(type(researcher), researcher)
    GraduateProgramResearcherSQL.delete(
        (researcher[0]["lattes_id"]), researcher[0]["graduate_program_id"]
    )
    return jsonify("Ok"), 200


@graduateProgramResearcherRest.route(
    "/GraduateProgramResearcherRest/Query/Count", methods=["GET"]
)
@cross_origin(origin="*", headers=["Content-Type"])
def query_count():
    institution_id = GraduateProgramResearcherSQL.query(
        request.args.get("institution_id")
    )

    count = GraduateProgramResearcherSQL.query_count(institution_id)
    return jsonify(count), 200
