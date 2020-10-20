from flask import Flask
from .user import users

def init_routes(app):
    app.register_blueprint(users)