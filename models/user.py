from database.db import db

class User(db.Document):
    name = db.StringField(required=True, max_length=50)
    surname = db.StringField(required=True, max_length=50)
    usr = db.StringField(required=True, unique=True, max_length=50)
    pwd = db.StringField(required=True)
    type_= db.IntField(required=True) # 0 - normal, 1 - admin