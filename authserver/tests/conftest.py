from typing import Generator

# noinspection Mypy
import pytest
from flask.testing import FlaskClient

from authserver import app, db
from authserver.tests import delete_rmq_test_users


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db.drop_all()
    db.create_all()

    delete_rmq_test_users()

    with app.test_client() as client:
        yield client
