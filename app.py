from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec

from Rest.graduateProgramResearcherRest import graduateProgramResearcherRest
from Rest.graduateProgramRest import graduateProgramRest
from Rest.institutionRest import institutionRest
from Rest.researcherRest import researcherRest

app = Flask(__name__)

api_spec = FlaskPydanticSpec("Flask", title="Api - Administrativo")
api_spec.register(app)

app.register_blueprint(institutionRest)
app.register_blueprint(researcherRest)
app.register_blueprint(graduateProgramRest)
app.register_blueprint(graduateProgramResearcherRest)


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify("OK"), 200


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        host="0.0.0.0",
    )
