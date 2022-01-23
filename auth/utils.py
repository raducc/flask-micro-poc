import jwt
from flask import current_app

from auth.models import Users


def get_user_from_token(token):
    try:
        data = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms="HS256",
        )
        return Users.query.filter_by(id=data["id"]).first()
    except Exception:
        return None
