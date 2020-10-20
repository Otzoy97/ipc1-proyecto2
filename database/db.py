from flask_mongoengine import MongoEngine

db = MongoEngine()

def initilize_db(app):
    db.init_app(app)