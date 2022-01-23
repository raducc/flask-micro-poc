from flask import Flask

from auth.models import db
from math_api.utils import cache
from math_api.views import math_api_app
from auth.views import auth_app
import os

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

db.init_app(app)
db.app = app

cache.init_app(app)
cache.app = app


app.register_blueprint(math_api_app)
app.register_blueprint(auth_app)

db.create_all()
db.session.commit()

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    app.run(host=host, port=port)
