from functools import wraps

import jwt
from flask import request, jsonify, current_app

from auth.models import Users
from auth.utils import get_user_from_token


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if "x-access-tokens" in request.headers:
            token = request.headers["x-access-tokens"]

        if not token:
            return jsonify({"message": "a valid token is missing"})

        current_user = get_user_from_token(token)
        if not current_user:
            return jsonify({"message": "token is invalid"})

        return f(current_user, *args, **kwargs)

    return decorator
