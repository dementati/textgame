import uuid

from flask import Response
from flask.testing import FlaskClient

from authserver.model.user import User
from authserver.rabbitmq import RabbitMQ

VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "H3ll0 w0rld!"


def delete_rmq_test_users() -> None:
    rmq = RabbitMQ()
    test_users = [user["name"] for user in rmq.users if user["name"].endswith("@example.com")]
    rmq.delete_users(test_users)


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


def random_valid_email() -> str:
    return f"{uuid.uuid4()}@example.com"
