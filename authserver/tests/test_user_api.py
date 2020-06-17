from typing import Generator

# noinspection Mypy
import pytest
from flask import Response
from flask.testing import FlaskClient

from authserver.model.user import User
from authserver.user_api import app, db

VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "abc123"


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db.drop_all()
    db.create_all()

    with app.test_client() as client:
        yield client


def test_create_email_persisted(client: FlaskClient) -> None:
    # GIVEN
    email = VALID_EMAIL

    # WHEN
    create_user_successfully(client, email)

    # THEN
    user = get_user_by_email(email)
    assert user.email == email


def test_create_empty_email(client: FlaskClient) -> None:
    # GIVEN
    email = ""

    # WHEN
    create_user_unsuccessfully(client, email)


def create_user_successfully(
        client: FlaskClient,
        email: str = VALID_EMAIL,
        password: str = VALID_PASSWORD
) -> Response:
    # GIVEN
    data = {
        "email": email,
        "password": password,
    }

    # WHEN
    rsp = client.post("/api/user", json=data)

    # THEN
    assert rsp.status_code == 200
    assert rsp.content_type == "application/json"
    assert "topic" in rsp.json

    return rsp


def create_user_unsuccessfully(
        client: FlaskClient,
        email: str = VALID_EMAIL,
        password: str = VALID_PASSWORD
) -> Response:
    # GIVEN
    data = {
        "email": email,
        "password": password,
    }

    # WHEN
    rsp = client.post("/api/user", json=data)

    # THEN
    assert rsp.status_code == 400
    assert rsp.content_type == "application/json"

    return rsp


def get_user_by_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()
    assert user is not None
    return user
