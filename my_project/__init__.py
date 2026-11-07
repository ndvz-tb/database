import os
import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)

    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "app.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    db_cfg = cfg["database"]
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_cfg['user']}:{db_cfg['password']}"
        f"@{db_cfg['host']}:{db_cfg['port']}/{db_cfg['database']}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cfg["flask"].get("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.json.ensure_ascii = False

    db.init_app(app)

    from my_project.auth.route import register_routes
    register_routes(app)

    return app
