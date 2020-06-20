import re
from typing import Tuple

import bcrypt
import email_validator
from flask import request, jsonify
from password_validator import PasswordValidator

from authserver import app, db
from authserver.model.user import User
from authserver.rabbitmq import RabbitMQ
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


@app.route('/api/user', methods=["POST"])
def create() -> Tuple[str, int]:
    body = request.json
    validate_create(body)
    user = create_db_user(body["email"], body["password"])
    create_rmq_user(body["email"], body["password"], user.hashed_id)
    return jsonify(dict(topic=f"user.{user.hashed_id}.message"))


def create_db_user(email: str, password: str) -> User:
    user = User(
        email=normalize_email(email),
        password=hash_password(password),
    )

    db.session.add(user)
    db.session.commit()

    user.hashed_id = hash_id(user.id)
    db.session.add(user)
    db.session.commit()

    return user


def create_rmq_user(email: str, password: str, hashed_id: str) -> None:
    rmq = RabbitMQ()
    rmq.put_user(email, password)
    rmq.put_topic_permissions(
        email,
        write=r"^.*%s.*$" % re.escape(hashed_id),
        read=r"^.*%s.*$" % re.escape(hashed_id),
    )


def validate_create(body: dict) -> None:
    # Validate email
    try:
        email = normalize_email(body["email"])
    except email_validator.EmailNotValidError:
        raise ValidationException("Invalid e-mail")

    if email_exists(email):
        raise ValidationException("E-mail already exists")

    # Validate password
    if not password_schema.validate(body["password"]):
        raise ValidationException("Invalid password. Must be at least 12 characters. "
                                  "Must include uppercase, lowercase, numbers and symbols")


def email_exists(email: str) -> bool:
    return bool(User.query.filter_by(email=email).first())


def normalize_email(email: str) -> str:
    return email_validator.validate_email(email).email


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def hash_id(db_id: int) -> str:
    bytes_id = str(db_id).encode("utf-8")
    hashed_id = bcrypt.hashpw(bytes_id, bcrypt.gensalt())
    return hashed_id.decode("utf-8")
