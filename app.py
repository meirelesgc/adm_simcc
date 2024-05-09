from flask import Flask, jsonify

from Rest.graduateProgramResearcherRest import graduateProgramResearcherRest
from Rest.graduateProgramRest import graduateProgramRest
from Rest.ind_prod import ind_prod
from Rest.institutionRest import institutionRest
from Rest.researcherRest import researcherRest
from Rest.researchGroupRest import researchGroupRest
from Rest.studentRest import studentRest

app = Flask(__name__)


app.register_blueprint(institutionRest)
app.register_blueprint(researcherRest)
app.register_blueprint(graduateProgramRest)
app.register_blueprint(graduateProgramResearcherRest)
app.register_blueprint(researchGroupRest)
app.register_blueprint(studentRest)
app.register_blueprint(ind_prod)


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify("OK"), 200


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        host="0.0.0.0",
    )
