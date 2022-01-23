import datetime

import jwt
from flask import Blueprint, request, jsonify, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Users

auth_app = Blueprint("auth", __name__)


@auth_app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    try:
        username = data["username"]
        password = data["password"]
    except (AttributeError, KeyError):
        return "error"

    if not (username and password):
        return "error"

    hashed_password = generate_password_hash(password, method="sha256")
    new_user = Users(name=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "registered successfully"})


@auth_app.route("/signup", methods=["GET"])
def signup_info():
    return 'Json content with {"username": "jondoe", "password": "pass"} required'


@auth_app.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not (auth and auth.username and auth.password):
        return make_response(
            "could not verify",
            401,
            {"WWW.Authentication": 'Basic realm: "login required"'},
        )

    user = Users.query.filter_by(name=auth.username).first()

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                "id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
        )
        return jsonify({"token": token})

    return make_response(
        "could not verify", 401, {"WWW.Authentication": 'Basic realm: "login required"'}
    )


@auth_app.route("/login", methods=["GET"])
def login_info():
    return "Basic Auth"
