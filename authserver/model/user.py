from authserver.user_api import db


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
