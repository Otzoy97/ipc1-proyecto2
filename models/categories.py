from database.db import db

class Category(db.Document):
    name = db.StringField(unique = True)