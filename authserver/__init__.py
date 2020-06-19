from flask import Flask, jsonify
# noinspection Mypy
from flask_sqlalchemy import SQLAlchemy

from common.error import ValidationException

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.model"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.errorhandler(ValidationException)
def handle_invalid_request(error):
    response = jsonify(error.as_dict())
    response.status_code = error.status_code
    return response
