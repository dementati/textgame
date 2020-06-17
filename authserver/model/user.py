from authserver.user_api import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, password={self.password})>"
