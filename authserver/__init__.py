from flask import Flask
# noinspection Mypy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.model"
db = SQLAlchemy(app)
