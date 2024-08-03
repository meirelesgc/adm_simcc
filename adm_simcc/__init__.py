from flask import Flask, jsonify
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

    return app
