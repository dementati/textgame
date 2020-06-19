from typing import Tuple

import bcrypt
from email_validator import validate_email, EmailNotValidError
from flask import request, jsonify
from password_validator import PasswordValidator

from authserver import app, db
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

    # Validate
    validate_create(body)

    # Write to database
    from authserver.model.user import User
    user = User(
        email=normalize_email(body["email"]),
        password=hash_password(body["password"]),
    )

    db.session.add(user)
    db.session.commit()

    # Hash ID and write to database
    user.hashed_id = hash_id(user.id)
    db.session.add(user)
    db.session.commit()

    # Return response
    rsp = {
        "topic": f"client.{user.id}.message"
    }

    return jsonify(rsp)


def validate_create(body: dict) -> None:
    try:
        validate_email(body["email"])
    except EmailNotValidError:
        raise ValidationException("Invalid email")

    if not password_schema.validate(body["password"]):
        raise ValidationException("Invalid password. Must be at least 12 characters. "
                                  "Must include uppercase, lowercase, numbers and symbols")


def normalize_email(email: str) -> str:
    return validate_email(email).email


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def hash_id(db_id: int) -> bytes:
    return bcrypt.hashpw(str(db_id).encode("utf-8"), bcrypt.gensalt())
