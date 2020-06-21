from typing import Optional

import bcrypt

from authserver import db
from common import email_utils


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    hashed_id = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self) -> str:
        return (
            f"<User("
            f"id={self.id}, "
            f"hashed_id={self.hashed_id}, "
            f"email={self.email}, "
            f"password={self.password}"
            f")>"
        )

    @classmethod
    def create(cls, email: str, password: str) -> "User":
        user = cls(
            email=email_utils.normalize(email),
            password=cls.hash_password(password),
        )

        db.session.add(user)
        db.session.commit()

        user.hashed_id = cls.hash_id(user.id)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get_by_email(cls, email: str) -> Optional["User"]:
        normal_email = email_utils.normalize(email)
        return cls.query.filter_by(email=normal_email).first()

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password, self.password)

    @staticmethod
    def hash_id(db_id: int) -> str:
        bytes_id = str(db_id).encode("utf-8")
        hashed_id = bcrypt.hashpw(bytes_id, bcrypt.gensalt())
        return hashed_id.decode("utf-8")
