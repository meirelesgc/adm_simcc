import os
import pandas as pd

from flask import jsonify, request, Blueprint
from flask_cors import cross_origin

from datetime import datetime
from werkzeug.utils import secure_filename

from Model.ResearchGroup import ResearchGroup

import Dao.ResearcherSQL as ResearcherSQL
import Dao.InstitutionSQL as InstitutionSQL
from Dao import ResearchGroupSQL

researchGroupRest = Blueprint("researchGroupRest", __name__)

@researchGroupRest.route("/researchGroupRest/Query", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def Query():
    try:
        JsonResearchGroups = []
        dfResearchGroups = ResearchGroupSQL.Query()

        for index, research_group_data in dfResearchGroups.iterrows():
            research_group_inst = ResearchGroup()
            research_group_inst.research_group_id = research_group_data["research_group_id"]
            research_group_inst.research_group_name = research_group_data["research_group_name"]
            research_group_inst.researcher_id = research_group_data["researcher_id"]
            research_group_inst.leader_name = research_group_data["leader_name"]
            research_group_inst.institution_name = research_group_data["institution_name"]
            research_group_inst.acronym = research_group_data["acronym"]
            research_group_inst.area = research_group_data["area"]
            research_group_inst.last_date_sent = research_group_data["last_date_sent"]
            research_group_inst.situation = research_group_data["situation"]
            research_group_inst.lattes_id = research_group_data["lattes_id"]
            research_group_inst.institution_id = research_group_data["institution_id"]

            JsonResearchGroups.append(research_group_inst.get_json())

        return jsonify(JsonResearchGroups), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Ocorreu um erro ao buscar os grupos de pesquisa'}), 500

@researchGroupRest.route("/researchGroupRest/QueryById", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def QueryById():

    research_group_id = request.args.get("research_group_id")

    if not research_group_id:
        return jsonify({"error": "Erro no Json enviado"}), 400
    
    try:
        JsonResearchGroups = []
        dfResearchGroups = ResearchGroupSQL.QueryById(research_group_id)
        for index, research_group_data in dfResearchGroups.iterrows():
            research_group_inst = ResearchGroup()
            research_group_inst.research_group_id = research_group_data["research_group_id"]
            research_group_inst.research_group_name = research_group_data["research_group_name"]
            research_group_inst.researcher_id = research_group_data["researcher_id"]
            research_group_inst.leader_name = research_group_data["leader_name"]
            research_group_inst.institution_name = research_group_data["institution_name"]
            research_group_inst.acronym = research_group_data["acronym"]
            research_group_inst.area = research_group_data["area"]
            research_group_inst.last_date_sent = research_group_data["last_date_sent"]
            research_group_inst.situation = research_group_data["situation"]
            research_group_inst.lattes_id = research_group_data["lattes_id"]
            research_group_inst.institution_id = research_group_data["institution_id"]

            JsonResearchGroups.append(research_group_inst.get_json())

        return jsonify(JsonResearchGroups), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Ocorreu um erro ao buscar o grupo de pesquisa por ID'}), 500


@researchGroupRest.route("/researchGroupRest/QueryByReseacherId", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def QueryByReseacherId():
    researcher_id = request.args.get("researcher_id")

    if not researcher_id:
        return jsonify({"error": "Erro no Json enviado"}), 400

    try:
        JsonResearchGroups = []

        dfResearchGroups = ResearchGroupSQL.QueryByReseacherId(researcher_id)
        for index, research_group_data in dfResearchGroups.iterrows():
            research_group_inst = ResearchGroup()
            research_group_inst.research_group_id = research_group_data["research_group_id"]
            research_group_inst.research_group_name = research_group_data["research_group_name"]
            research_group_inst.researcher_id = research_group_data["researcher_id"]
            research_group_inst.leader_name = research_group_data["leader_name"]
            research_group_inst.institution_name = research_group_data["institution_name"]
            research_group_inst.acronym = research_group_data["acronym"]
            research_group_inst.area = research_group_data["area"]
            research_group_inst.last_date_sent = research_group_data["last_date_sent"]
            research_group_inst.situation = research_group_data["situation"]
            research_group_inst.lattes_id = research_group_data["lattes_id"]
            research_group_inst.institution_id = research_group_data["institution_id"]

            JsonResearchGroups.append(research_group_inst.get_json())

        return jsonify(JsonResearchGroups), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Ocorreu um erro ao buscar os grupos de pesquisa por ID do pesquisador'}), 500


@researchGroupRest.route("/researchGroupRest/QueryByInstitutionId", methods=["GET"])
@cross_origin(origin="*", headers=["Content-Type"])
def QueryByInstitutionId():
    institution_id = request.args.get("institution_id")

    if not institution_id:
        return jsonify({"error": "Erro no Json enviado"}), 400

    try:
        JsonResearchGroups = []

        dfResearchGroups = ResearchGroupSQL.QueryByInstitutionId(institution_id)
        for index, research_group_data in dfResearchGroups.iterrows():
            research_group_inst = ResearchGroup()
            research_group_inst.research_group_id = research_group_data["research_group_id"]
            research_group_inst.research_group_name = research_group_data["research_group_name"]
            research_group_inst.researcher_id = research_group_data["researcher_id"]
            research_group_inst.leader_name = research_group_data["leader_name"]
            research_group_inst.institution_name = research_group_data["institution_name"]
            research_group_inst.acronym = research_group_data["acronym"]
            research_group_inst.area = research_group_data["area"]
            research_group_inst.last_date_sent = research_group_data["last_date_sent"]
            research_group_inst.situation = research_group_data["situation"]
            research_group_inst.lattes_id = research_group_data["lattes_id"]
            research_group_inst.institution_id = research_group_data["institution_id"]

            JsonResearchGroups.append(research_group_inst.get_json())

        return jsonify(JsonResearchGroups), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Ocorreu um erro ao buscar os grupos de pesquisa por ID do pesquisador'}), 500




@researchGroupRest.route("/researchGroupRest/Insert", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def Insert():
    if 'file' not in request.files:
        return jsonify({'error': 'Sem arquivo na requisição'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Sem arquivo na requsição'}), 400

    if file:
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        allowed_extensions = ['xlsx', 'xls']
        if extension not in allowed_extensions:
            return jsonify({'error': 'Tipo de arquivo não permitido'}), 400

        current_dir = os.path.dirname(os.path.abspath(__file__))
        upload_folder = os.path.join(current_dir, '..' , "research_group_files")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        try:
            filename_with_timestamp = str(datetime.now().strftime("%d%m%Y%H%M%S") + '_' + filename  )
            file_path = os.path.join(upload_folder, filename_with_timestamp)
            file.save(file_path)
        except Exception as e:
            print(f"Erro:  {e}")
            return jsonify({'error': 'Ocorreu um erro ao realizar o uplaod do arquivo'}), 400
        
        try:
            dfResearchGroups = pd.read_excel(file_path, skiprows=2, skipfooter=1).fillna('')
            for index, research_group_data in dfResearchGroups.iterrows():
                research_group_inst = ResearchGroup()
                research_group_inst.research_group_name = research_group_data["Nome do Grupo"]                        
                research_group_inst.researcher_id = ResearcherSQL.QueryByName(research_group_data["Nome do Líder"])
                research_group_inst.institution_id = InstitutionSQL.QueryByName(research_group_data["Instituição"])
                research_group_inst.area = research_group_data["Área Predominante"]
                research_group_inst.last_date_sent = research_group_data["Último Envio"]
                research_group_inst.situation = research_group_data["Situação"]
                research_group_inst.file_path = file_path
                print(f"Inserindo grupo de pesquisa - {research_group_inst.research_group_name} id: {research_group_inst.researcher_id}")
                ResearchGroupSQL.Insert(research_group_inst)
            return jsonify("Inserção dos grupos de pesquisa bem sucedida"), 200
        except Exception as e:
            print(f"Erro: {e}")
            return jsonify({'error': 'Ocorreu um erro ao cadastrar os dados do arquivo Excel'}), 400
    
    return jsonify({'error': 'Ocorreu um erro interno ao processar os dados do arquivo'}), 400


@researchGroupRest.route("/researchGroupRest/Delete", methods=["DELETE"])
@cross_origin(origin="*", headers=["Content-Type"])
def Delete():

    research_group_id = request.args.get("research_group_id")

    if not research_group_id:
        return jsonify({"error": "Erro no Json enviado"}), 400

    try:
        ResearchGroupSQL.Delete(research_group_id)
        return jsonify("Exclusão bem-sucedida"), 200

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': 'Ocorreu um erro ao excluir o grupo de pesquisa'}), 500
