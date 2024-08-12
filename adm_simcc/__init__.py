from flask import Flask, jsonify, request
from flask_cors import CORS
from http import HTTPStatus


def create_app():
    app = Flask(__name__)

    from .rest.rest_graduate_program import rest_graduate_program
    from .rest.rest_gradute_program_researcher import rest_graduate_program_researcher
    from .rest.rest_graduate_program_student import rest_graduate_program_student
    from .rest.rest_ind_prod import rest_ind_prod
    from .rest.rest_institution import rest_institution
    from .rest.rest_researcher import rest_researcher
    from .rest.rest_researcher_group import rest_researcher_group
    from .rest.rest_system_management import rest_system
    from .rest.rest_teacher import rest_teacher
    from .rest.rest_technician import rest_technician
    from .rest.rest_departament import rest_departament

    app.register_blueprint(rest_researcher_group)
    app.register_blueprint(rest_institution)
    app.register_blueprint(rest_researcher)
    app.register_blueprint(rest_graduate_program)
    app.register_blueprint(rest_graduate_program_researcher)
    app.register_blueprint(rest_graduate_program_student)
    app.register_blueprint(rest_ind_prod)
    app.register_blueprint(rest_system)
    app.register_blueprint(rest_teacher)
    app.register_blueprint(rest_technician)
    app.register_blueprint(rest_departament)

    CORS(app)

    @app.route("/", methods=["GET"])
    def home():

        response_data = {"message": "api em funcionamento"}
        return jsonify(response_data), HTTPStatus.OK

    @app.route("/login", methods=["GET"])
    def login():
        user_data = {
            "application_id":
            request.headers.get('Shib-Application-ID'),
            "session_id":
            request.headers.get('Shib-Session-ID'),
            "identity_provider":
            request.headers.get('Shib-Identity-Provider'),
            "authentication_instant":
            request.headers.get('Shib-Authentication-Instant'),
            "authentication_method":
            request.headers.get('Shib-Authentication-Method'),
            "authn_context_class":
            request.headers.get('Shib-AuthnContext-Class'),
            "session_index":
            request.headers.get('Shib-Session-Index'),
            "org_dn":
            request.headers.get('Shib-EP-OrgDN'),
            "org_unit_dn":
            request.headers.get('Shib-EP-OrgUnitDN'),
            "primary_affiliation":
            request.headers.get('Shib-EP-PrimaryAffiliation'),
            "given_name":
            request.headers.get('Shib-InetOrgPerson-givenName'),
            "common_name":
            request.headers.get('Shib-Person-CommonName'),
            "email":
            request.headers.get('Shib-Person-Mail'),
            "uid":
            request.headers.get('Shib-Person-UID'),
            "surname":
            request.headers.get('Shib-Person-surname'),
            "cpf":
            request.headers.get('Shib-brPerson-CPF'),
            "curso_nivel":
            request.headers.get('Shib-brPerson-CursoNivel'),
            "data_nascimento":
            request.headers.get('Shib-brPerson-DataNascimento'),
            "sexo":
            request.headers.get('Shib-brPerson-Sexo'),
            "status":
            request.headers.get('Shib-ufmgPerson-Status'),
            "url_email":
            request.headers.get('Shib-ufmgPerson-URLEmail')
        }
        return jsonify(user_data)

    return app
