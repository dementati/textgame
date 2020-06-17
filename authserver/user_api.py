from typing import Tuple

from flask import request, jsonify

from authserver import app, db


@app.route('/api/user', methods=["POST"])
def create() -> Tuple[str, int]:
    body = request.json

    # Validate
    if not body["email"]:
        rsp = {"error_message": "Invalid email"}
        return jsonify(rsp), 400

    # Write to database
    from authserver.model.user import User
    user = User(
        email=body["email"],
        password=body["password"]
    )

    db.session.add(user)
    db.session.commit()

    # Return response
    rsp = {
        "topic": f"client.{user.id}.message"
    }

    return jsonify(rsp)
