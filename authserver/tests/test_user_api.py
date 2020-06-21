import re

# noinspection Mypy
import bcrypt
# noinspection Mypy
from flask.testing import FlaskClient

from authserver.rabbitmq import RabbitMQ
from authserver.tests import VALID_EMAIL, create_user_successfully, VALID_PASSWORD, create_user_unsuccessfully, \
    get_user_by_email, random_valid_email


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
    assert bcrypt.checkpw(str(user.id).encode("utf-8"), user.hashed_id.encode("utf-8"))


def test_create_existing_email(client: FlaskClient) -> None:
    # GIVEN
    email = VALID_EMAIL
    create_user_successfully(client, email=email)

    # WHEN/THEN
    create_user_unsuccessfully(client, email=email)


def test_create_rsp_contains_topic(client: FlaskClient) -> None:
    # GIVEN
    email = VALID_EMAIL

    # WHEN
    rsp = create_user_successfully(client)

    # THEN
    user = get_user_by_email(email)
    expected_topic = f"user.{user.hashed_id}.message"
    assert expected_topic == rsp.json["topic"]


def test_create_rmq_user_created(client: FlaskClient) -> None:
    # GIVEN
    email = random_valid_email()

    # WHEN
    create_user_successfully(client, email=email)

    # THEN
    rmq = RabbitMQ()
    assert any(user["name"] == email for user in rmq.users)


def test_create_rmq_topic_permission_set(client: FlaskClient) -> None:
    # GIVEN
    email = random_valid_email()

    # WHEN
    create_user_successfully(client, email=email)

    # THEN
    user = get_user_by_email(email)

    expected_write = r"^.*%s.*$" % re.escape(user.hashed_id)
    expected_read = r"^.*%s.*$" % re.escape(user.hashed_id)
    print(expected_write)
    permissions = RabbitMQ().get_topic_permissions(email)
    assert len(permissions) == 1
    permission = permissions[0]
    assert permission["user"] == email
    assert permission["write"] == expected_write
    assert permission["read"] == expected_read


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
