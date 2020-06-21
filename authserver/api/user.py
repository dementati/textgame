import re
from typing import Tuple

from flask import request, jsonify, Blueprint
from password_validator import PasswordValidator

from authserver.rabbitmq import RabbitMQ
from common import email_utils
from common.error import ValidationException

password_schema = PasswordValidator()

(
    password_schema.min(12)
                   .max(100)
                   .has().uppercase()
                   .has().lowercase()
                   .has().digits()
                   .has().symbols()
)


user_api = Blueprint("user_api", __name__)


@user_api.route('/api/user', methods=["POST"])
def create() -> Tuple[str, int]:
    from authserver.model.user import User

    body = request.json
    validate_create(body)
    user = User.create(body["email"], body["password"])
    create_rmq_user(body["email"], body["password"], user.hashed_id)
    return jsonify(dict(topic=f"user.{user.hashed_id}.message"))


def create_rmq_user(email: str, password: str, hashed_id: str) -> None:
    rmq = RabbitMQ()
    rmq.put_user(email, password)
    rmq.put_topic_permissions(
        email,
        write=r"^.*%s.*$" % re.escape(hashed_id),
        read=r"^.*%s.*$" % re.escape(hashed_id),
    )


def validate_create(body: dict) -> None:
    from authserver.model.user import User

    # Validate email
    if not email_utils.is_valid(body["email"]):
        raise ValidationException("Invalid e-mail")

    if User.get_by_email(body["email"]):
        raise ValidationException("E-mail already exists")

    # Validate password
    if not password_schema.validate(body["password"]):
        raise ValidationException("Invalid password. Must be at least 12 characters. "
                                  "Must include uppercase, lowercase, numbers and symbols")
