from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def default():
    return jsonify("Modulo administrativo em funcionamento!"), 200
