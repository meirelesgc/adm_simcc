from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    response_data = {"message": "api em funcionamento"}
    return jsonify(response_data), HTTPStatus.OK


def create_app():
    app = Flask(__name__)

    from .rest.rest_graduate_program import rest_graduate_program
    from .rest.rest_gradute_program_researcher import rest_graduate_program_researcher
    from .rest.rest_ind_prod import rest_ind_prod
    from .rest.rest_institution import rest_institution
    from .rest.rest_researcher import rest_researcher
    from .rest.rest_student import rest_student
    from .rest.rest_researcher_group import rest_researcher_group

    app.register_blueprint(rest_researcher_group)
    app.register_blueprint(rest_institution)
    app.register_blueprint(rest_researcher)
    app.register_blueprint(rest_graduate_program)
    app.register_blueprint(rest_graduate_program_researcher)
    app.register_blueprint(rest_student)
    app.register_blueprint(rest_ind_prod)

    @app.route("/abc", methods=["GET"])
    def home():
        print(request.args.get("abc", "bcd"))
        response_data = {"message": "api em funcionamento"}
        return jsonify(response_data), HTTPStatus.OK

    return app
