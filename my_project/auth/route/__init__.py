from flask import Flask
from my_project.auth.route.orders_route import api_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(api_bp)
