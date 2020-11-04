from flask import Flask
from .user import users
from .application import apps
from .category import cats

def init_routes(app):
    app.register_blueprint(users)
    app.register_blueprint(apps)
    app.register_blueprint(cats)