from database.db import db
from .categories import Category

class Application(db.Document):
    title = db.StringField()
    url = db.URLField()
    cat = db.ReferenceField(Category)
    downloads = db.IntField()
    des = db.StringField()
    price = db.DecimalField()
    likes = db.IntField()