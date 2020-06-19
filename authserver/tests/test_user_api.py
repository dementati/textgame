from typing import Generator

# noinspection Mypy
import bcrypt
# noinspection Mypy
import pytest
from flask import Response
from flask.testing import FlaskClient

from authserver.model.user import User
from authserver.user_api import app, db

VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "H3ll0 w0rld!"


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
    create_user_successfully(client, email=email)

    # THEN
    user = get_user_by_email(email)
    assert user.email == email


def test_create_hashed_password_persisted(client: FlaskClient) -> None:
    # GIVEN
    email = VALID_EMAIL
    password = VALID_PASSWORD

    # WHEN
    create_user_successfully(client, email=email, password=password)

    # THEN
    user = get_user_by_email(email)
    assert bcrypt.checkpw(password.encode("utf-8"), user.password)


def test_create_hashed_id_persisted(client: FlaskClient) -> None:
    # GIVEN
    email = VALID_EMAIL

    # WHEN
    create_user_successfully(client)

    # THEN
    user = get_user_by_email(email)
    assert bcrypt.checkpw(str(user.id).encode("utf-8"), user.hashed_id)


def test_create_empty_email(client: FlaskClient) -> None:
    # GIVEN
    email = ""

    # WHEN
    create_user_unsuccessfully(client, email=email)


def test_create_non_email(client: FlaskClient) -> None:
    # GIVEN
    email = "foobarbaz"

    # WHEN
    create_user_unsuccessfully(client, email=email)


def test_create_empty_password(client: FlaskClient) -> None:
    # GIVEN
    password = ""

    # WHEN
    create_user_unsuccessfully(client, password=password)


def test_create_password_with_no_digits(client: FlaskClient) -> None:
    # GIVEN
    password = "Hello world!"

    # WHEN
    create_user_unsuccessfully(client, password=password)


def test_create_password_with_no_uppercase(client: FlaskClient) -> None:
    # GIVEN
    password = "h3ll0 w0rld!"

    # WHEN
    create_user_unsuccessfully(client, password=password)


def test_create_password_with_no_lowercase(client: FlaskClient) -> None:
    # GIVEN
    password = "H3LL0 W0RLD!"

    # WHEN
    create_user_unsuccessfully(client, password=password)


def test_create_password_with_no_symbols(client: FlaskClient) -> None:
    # GIVEN
    password = "H3lllll0w0rld"

    # WHEN
    create_user_unsuccessfully(client, password=password)


def test_create_too_short_password(client: FlaskClient) -> None:
    # GIVEN
    password = "H3ll0 w0rl!"

    # WHEN
    create_user_unsuccessfully(client, password=password)


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
