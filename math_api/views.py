from flask import Blueprint, request, current_app, url_for, jsonify, make_response

from auth.decorators import token_required
from .utils import get_fibonacci, get_factorial

math_api_app = Blueprint("", __name__)


@math_api_app.route("/pow", methods=["GET"], strict_slashes=False)
@token_required
def power(current_user):
    args = request.args
    try:
        base = float(args.get("base"))
        exp = float(args.get("exp"))
    except TypeError:
        return make_response("GET args required: base, exp", 400)
    except ValueError:
        return make_response("Invalid values for 'base' and 'exp' args", 400)

    return f"{pow(base, exp)}"


@math_api_app.route("/fibonacci", methods=["GET"], strict_slashes=False)
@token_required
def fibonacci(current_user):
    args = request.args
    try:
        n = int(args.get("n"))
    except TypeError:
        return make_response("GET args required: n", 400)
    except ValueError:
        return make_response("Invalid value for 'n' arg", 400)
    fibo = get_fibonacci(n)
    return f"{fibo}"


@math_api_app.route("/factorial", methods=["GET"], strict_slashes=False)
# @token_required
# def factorial(current_user):
def factorial():
    args = request.args

    try:
        n = int(args.get("n"))
    except TypeError:
        return make_response("GET args required: n", 400)
    except ValueError:
        return make_response("Invalid value for 'n' arg", 400)

    if n < 0:
        return make_response("Invalid value for 'n' arg", 400)

    fact = get_factorial(n)
    return f"{fact}"


@math_api_app.route("/site-map", methods=["GET"], strict_slashes=False)
def site_map():
    output = []
    for rule in current_app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ",".join(rule.methods & {"GET", "POST"})
        url = url_for(rule.endpoint, **options)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    lines = []
    for line in sorted(output):
        lines.append(line)
    return jsonify({"routes": lines})
