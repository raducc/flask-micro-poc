from functools import wraps

import jwt
from flask import request, jsonify, current_app

from auth.models import Users


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})

        try:
            # return current_app.config["SECRET_KEY"]
            # ff = jwt.decode(
            #     "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjQyOTQ2OTMxfQ.X0WDUeM1KOuPfCx1mKtpYE4e_C6E-s7I7-PuLEHbVO8",
            #     current_app.config["SECRET_KEY"],
            #     algorithms="HS256",
            # )
            # return ff
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms="HS256",
            )
            current_user = Users.query.filter_by(id=data["id"]).first()
        except Exception as e:
            return str(e)
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)

    return decorator
