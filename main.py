from datetime import datetime

from flask import Flask, request

from auth.models import db
from auth.utils import get_user_from_token
from math_api.utils import cache
from math_api.views import math_api_app
from auth.views import auth_app
import os
from elasticsearch import Elasticsearch


app = Flask(__name__)

app.config.update(
    {
        "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://{}:{}@{}/{}".format(
            os.getenv("DB_USER", "flask"),
            os.getenv("DB_PASSWORD", "password123"),
            os.getenv("DB_HOST", "mysql"),
            os.getenv("DB_NAME", "flask"),
        ),
        "DEBUG": True,
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300,
    }
)
app.config["SECRET_KEY"] = "cccsc"

es = Elasticsearch([{"host": "host.docker.internal", "port": 9200}])

db.init_app(app)
db.app = app

cache.init_app(app)
cache.app = app


app.register_blueprint(math_api_app)
app.register_blueprint(auth_app)

db.create_all()
db.session.commit()


@app.before_request
def before_request_signal():
    current_user = get_user_from_token(request.headers.get("x-access-tokens"))

    user_id = current_user.pk if current_user else None
    body = {
        "path": request.path,
        "method": request.method,
        "user": user_id,
        "args": {k: v for k, v in request.args.items()},
        "timestamp": datetime.now(),
    }
    es.index(index="requests", document=body)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    app.run(host=host, port=port)
