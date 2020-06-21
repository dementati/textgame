from flask import Flask, jsonify
# noinspection Mypy
from flask_sqlalchemy import SQLAlchemy

from authserver.api.user import user_api
from common.error import ValidationException

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.model"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db: SQLAlchemy = SQLAlchemy(app)

app.register_blueprint(user_api)


@app.errorhandler(ValidationException)
def handle_invalid_request(error: ValidationException) -> None:
    response = jsonify(error.as_dict())
    response.status_code = error.status_code
    return response
