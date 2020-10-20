from flask import Flask
from .movie import movies
from .user import users

def init_routes(app):
    app.register_blueprint(users)